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
 */
export async function recordGamificationAnswer(
  uid: string | null,
  correct: boolean,
  mode: 'practice' | 'challenge' | 'review',
  currentStreak: number, // streak from game engine
): Promise<RecordAnswerResult> {
  const prev = uid ? await firestoreLoad(uid) : localLoad();
  let data = updateDailyStreak(prev);

  // ── XP calculation ──────────────────────────────────────────────────────
  let xp = 0;
  if (correct) {
    const base = mode === 'challenge' ? 15 : mode === 'review' ? 12 : 10;
    const streakBonus = Math.min(currentStreak, 10) * 2; // up to +20
    xp = base + streakBonus;
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
  const newBadges = checkNewBadges(prev, data, currentLevel);
  data = { ...data, badgesEarned: [...data.badgesEarned, ...newBadges] };

  // ── Persist ─────────────────────────────────────────────────────────────
  if (uid) await firestoreSave(uid, data);
  localSave(data);

  return { xpGained: xp, newBadges, leveledUp, data };
}

/**
 * Record session completion (practice / challenge / teach / review).
 */
export async function recordSessionComplete(
  uid: string | null,
  type: 'practice' | 'challenge' | 'teach' | 'review',
): Promise<RecordAnswerResult> {
  const prev = uid ? await firestoreLoad(uid) : localLoad();
  let data = updateDailyStreak(prev);

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
  const newBadges = checkNewBadges(prev, data, currentLevel);
  data = { ...data, badgesEarned: [...data.badgesEarned, ...newBadges] };

  if (uid) await firestoreSave(uid, data);
  localSave(data);

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
