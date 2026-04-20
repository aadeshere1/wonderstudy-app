import { getFirestore, doc, getDoc, setDoc } from 'firebase/firestore';
import app from '@/lib/firebase/config';
import type { GamificationData } from './types';
import { DEFAULT_GAMIFICATION } from './types';
import { getLevelForXP } from './levels';
import { checkNewBadges } from './badges';
import { didLevelUp } from './levels';
import type { Level } from './types';


const LOCAL_KEY = 'ws_gam_v1';

// ── localStorage helpers ──────────────────────────────────────────────────

function localLoad(): GamificationData {
  try {
    const raw = localStorage.getItem(LOCAL_KEY);
    if (raw) return { ...DEFAULT_GAMIFICATION, ...JSON.parse(raw) };
  } catch {}
  return { ...DEFAULT_GAMIFICATION };
}

function localSave(data: GamificationData) {
  try { localStorage.setItem(LOCAL_KEY, JSON.stringify(data)); } catch {}
}

// ── Firestore helpers ─────────────────────────────────────────────────────

function gamRef(uid: string) {
  return doc(getFirestore(app), 'users', uid, 'gamification', 'data');
}

async function firestoreLoad(uid: string): Promise<GamificationData> {
  try {
    const snap = await getDoc(gamRef(uid));
    if (snap.exists()) return { ...DEFAULT_GAMIFICATION, ...snap.data() } as GamificationData;
  } catch {}
  return { ...DEFAULT_GAMIFICATION };
}

async function firestoreSave(uid: string, data: GamificationData) {
  try { await setDoc(gamRef(uid), data); } catch {}
}

// ── Debounced Firestore write ─────────────────────────────────────────────
// localStorage is always written synchronously; Firestore is written after 3 s
// of idle time so rapid answering only produces one write per burst.

let _debounceTimer: ReturnType<typeof setTimeout> | null = null;
let _pendingSave: { uid: string; data: GamificationData } | null = null;

function scheduleSave(uid: string, data: GamificationData): void {
  _pendingSave = { uid, data };
  if (_debounceTimer) clearTimeout(_debounceTimer);
  _debounceTimer = setTimeout(() => {
    _debounceTimer = null;
    if (_pendingSave) {
      firestoreSave(_pendingSave.uid, _pendingSave.data).catch(console.error);
      _pendingSave = null;
    }
  }, 3000);
}

/**
 * Immediately flush any pending debounced Firestore write.
 * Call this at session end so the final state is persisted before the page
 * navigates away.
 */
export function flushGamificationSave(): void {
  if (_debounceTimer) {
    clearTimeout(_debounceTimer);
    _debounceTimer = null;
  }
  if (_pendingSave) {
    firestoreSave(_pendingSave.uid, _pendingSave.data).catch(console.error);
    _pendingSave = null;
  }
}

// ── Today ISO helper ──────────────────────────────────────────────────────

function todayISO(): string {
  return new Date().toISOString().split('T')[0];
}

function yesterdayISO(): string {
  const d = new Date();
  d.setDate(d.getDate() - 1);
  return d.toISOString().split('T')[0];
}

// ── Daily streak update ───────────────────────────────────────────────────

function updateDailyStreak(data: GamificationData): GamificationData {
  const today = todayISO();
  if (data.lastPlayDate === today) return data; // already counted today
  const newDailyStreak = data.lastPlayDate === yesterdayISO()
    ? data.dailyStreak + 1
    : 1;
  return { ...data, lastPlayDate: today, dailyStreak: newDailyStreak };
}

// ── Public API ────────────────────────────────────────────────────────────

export async function loadGamification(uid: string | null): Promise<GamificationData> {
  return uid ? firestoreLoad(uid) : localLoad();
}

export interface RecordAnswerResult {
  xpGained: number;
  newBadges: string[];
  leveledUp: Level | null;
  data: GamificationData;
}

/**
 * Record a question answer. Returns XP gained, newly unlocked badges, and level-up info.
 *
 * Pass `prev` (the caller's current in-memory data) to skip the Firestore read.
 * If omitted, falls back to a Firestore/localStorage load.
 */
export async function recordGamificationAnswer(
  uid: string | null,
  correct: boolean,
  mode: 'practice' | 'challenge' | 'review',
  currentStreak: number, // streak from game engine
  prev?: GamificationData,
): Promise<RecordAnswerResult> {
  const base = prev ?? (uid ? await firestoreLoad(uid) : localLoad());
  let data = updateDailyStreak(base);

  // ── XP calculation ──────────────────────────────────────────────────────
  let xp = 0;
  if (correct) {
    const xpBase = mode === 'challenge' ? 15 : mode === 'review' ? 12 : 10;
    const streakBonus = Math.min(currentStreak, 10) * 2; // up to +20
    xp = xpBase + streakBonus;
  } else {
    xp = 1; // participation XP
  }

  const oldXP = data.totalXP;
  data = {
    ...data,
    totalXP: data.totalXP + xp,
    totalQuestions: data.totalQuestions + 1,
    totalCorrect: data.totalCorrect + (correct ? 1 : 0),
    currentStreak: correct ? data.currentStreak + 1 : 0,
    maxStreak: correct
      ? Math.max(data.maxStreak, data.currentStreak + 1)
      : data.maxStreak,
  };

  // ── Level check ─────────────────────────────────────────────────────────
  const leveledUp = didLevelUp(oldXP, data.totalXP);
  const currentLevel = getLevelForXP(data.totalXP).level;

  // ── Badge check ─────────────────────────────────────────────────────────
  const newBadges = checkNewBadges(base, data, currentLevel);
  data = { ...data, badgesEarned: [...data.badgesEarned, ...newBadges] };

  // ── Persist ─────────────────────────────────────────────────────────────
  // localStorage: always immediate
  localSave(data);
  // Firestore: debounced — only fires after 3 s of no new answers
  if (uid) scheduleSave(uid, data);

  return { xpGained: xp, newBadges, leveledUp, data };
}

/**
 * Record session completion (practice / challenge / teach / review).
 *
 * Pass `prev` to skip the Firestore read. Flushes any pending debounced write
 * before scheduling its own immediate write, so state is never lost.
 */
export async function recordSessionComplete(
  uid: string | null,
  type: 'practice' | 'challenge' | 'teach' | 'review',
  prev?: GamificationData,
): Promise<RecordAnswerResult> {
  // Flush any pending debounced answer write first so we build on the freshest data
  if (uid) flushGamificationSave();

  const base = prev ?? (uid ? await firestoreLoad(uid) : localLoad());
  let data = updateDailyStreak(base);

  const sessionXP = type === 'teach' ? 20 : type === 'review' ? 30 : 25;
  const oldXP = data.totalXP;

  data = {
    ...data,
    totalXP: data.totalXP + sessionXP,
    sessionsCompleted: type !== 'teach'
      ? data.sessionsCompleted + 1
      : data.sessionsCompleted,
    teachSessions: type === 'teach'
      ? data.teachSessions + 1
      : data.teachSessions,
    reviewSessions: type === 'review'
      ? data.reviewSessions + 1
      : data.reviewSessions,
  };

  const leveledUp = didLevelUp(oldXP, data.totalXP);
  const currentLevel = getLevelForXP(data.totalXP).level;
  const newBadges = checkNewBadges(base, data, currentLevel);
  data = { ...data, badgesEarned: [...data.badgesEarned, ...newBadges] };

  // Immediate write (session end is a natural sync point)
  localSave(data);
  if (uid) await firestoreSave(uid, data);

  return { xpGained: sessionXP, newBadges, leveledUp, data };
}

/**
 * Merge local data into Firestore on sign-in. Keep higher XP.
 */
export async function mergeLocalGamificationToFirestore(uid: string) {
  const local = localLoad();
  const remote = await firestoreLoad(uid);
  if (local.totalXP <= remote.totalXP) return; // remote is already ahead
  // Merge: take higher XP, union badges
  const merged: GamificationData = {
    ...remote,
    totalXP: Math.max(remote.totalXP, local.totalXP),
    totalQuestions: Math.max(remote.totalQuestions, local.totalQuestions),
    totalCorrect: Math.max(remote.totalCorrect, local.totalCorrect),
    maxStreak: Math.max(remote.maxStreak, local.maxStreak),
    badgesEarned: Array.from(new Set([...remote.badgesEarned, ...local.badgesEarned])),
    sessionsCompleted: Math.max(remote.sessionsCompleted, local.sessionsCompleted),
    teachSessions: Math.max(remote.teachSessions, local.teachSessions),
    reviewSessions: Math.max(remote.reviewSessions, local.reviewSessions),
    dailyStreak: Math.max(remote.dailyStreak, local.dailyStreak),
  };
  await firestoreSave(uid, merged);
}
