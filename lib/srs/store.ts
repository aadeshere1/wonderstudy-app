/**
 * Unified SRS store.
 * - Logged-in users  → reads/writes Firestore, keeps localStorage as cache
 * - Guest users       → localStorage only
 * - On sign-in        → merges local progress into Firestore (keeps later dueDate)
 */

import { SRSCard, SRSAllData } from './types';
import { applyAnswer, newCard, isDue } from './algorithm';

// ── Firestore imports (lazy to avoid SSR issues) ──────────────────────────────
async function getFirestore() {
  const { getFirestore: gf, doc, getDoc, setDoc } = await import('firebase/firestore');
  const app = (await import('@/lib/firebase/config')).default;
  return { db: gf(app), doc, getDoc, setDoc };
}

// ── localStorage helpers ──────────────────────────────────────────────────────
const LS_KEY = 'ws_srs_v1';

function localLoad(): SRSAllData {
  if (typeof window === 'undefined') return {};
  try {
    const raw = localStorage.getItem(LS_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch { return {}; }
}

function localSave(data: SRSAllData): void {
  if (typeof window === 'undefined') return;
  try { localStorage.setItem(LS_KEY, JSON.stringify(data)); } catch { /* quota */ }
}

// ── Firestore helpers ─────────────────────────────────────────────────────────
async function firestoreLoad(uid: string): Promise<SRSAllData> {
  try {
    const { db, doc, getDoc } = await getFirestore();
    const ref  = doc(db, 'users', uid, 'srs', 'progress');
    const snap = await getDoc(ref);
    return snap.exists() ? (snap.data() as SRSAllData) : {};
  } catch { return {}; }
}

async function firestoreSave(uid: string, data: SRSAllData): Promise<void> {
  try {
    const { db, doc, setDoc } = await getFirestore();
    const ref = doc(db, 'users', uid, 'srs', 'progress');
    await setDoc(ref, data, { merge: true });
  } catch (e) { console.error('Firestore save failed', e); }
}

// ── Merge: keep card with later dueDate ──────────────────────────────────────
function mergeData(local: SRSAllData, remote: SRSAllData): SRSAllData {
  const merged: SRSAllData = { ...remote };
  for (const [id, card] of Object.entries(local)) {
    if (!merged[id] || card.dueDate > merged[id].dueDate) {
      merged[id] = card;
    }
  }
  return merged;
}

// ── Public API ────────────────────────────────────────────────────────────────

/** Call once after sign-in to sync local → Firestore */
export async function mergeLocalToFirestore(uid: string): Promise<void> {
  const local  = localLoad();
  if (Object.keys(local).length === 0) return;
  const remote = await firestoreLoad(uid);
  const merged = mergeData(local, remote);
  await firestoreSave(uid, merged);
  localSave(merged);
}

/** Record an answer for a card. uid=null means guest (localStorage only). */
export async function recordAnswer(
  uid: string | null,
  lessonId: string,
  section: string,
  index: number,
  correct: boolean,
  hintUsed: boolean,
): Promise<void> {
  const quality = correct ? (hintUsed ? 3 : 5) : 1;
  const cardId  = `${lessonId}_${section}_${index}`;

  // load current data
  let data: SRSAllData;
  if (uid) {
    data = await firestoreLoad(uid);
  } else {
    data = localLoad();
  }

  const existing = data[cardId] ?? newCard(lessonId, section, index);
  const updated  = applyAnswer(existing, quality);
  data[cardId]   = updated;

  // save
  localSave(data);
  if (uid) await firestoreSave(uid, data);
}

/** Get all due cards for a specific lesson */
export async function getDueCards(
  uid: string | null,
  lessonId: string,
): Promise<SRSCard[]> {
  const data = uid ? await firestoreLoad(uid) : localLoad();
  return Object.values(data).filter(
    (c) => c.lessonId === lessonId && isDue(c)
  );
}

/** Get total due count across ALL lessons */
export async function getTotalDueCount(uid: string | null): Promise<number> {
  const data = uid ? await firestoreLoad(uid) : localLoad();
  return Object.values(data).filter(isDue).length;
}

/** Get all cards ever seen for a lesson (for progress display) */
export async function getLessonCards(
  uid: string | null,
  lessonId: string,
): Promise<SRSAllData> {
  const data = uid ? await firestoreLoad(uid) : localLoad();
  const result: SRSAllData = {};
  for (const [id, card] of Object.entries(data)) {
    if (card.lessonId === lessonId) result[id] = card;
  }
  return result;
}
