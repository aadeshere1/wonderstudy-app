/**
 * Unified SRS store — optimised for minimal Firestore usage.
 *
 * Read strategy  : in-memory cache (populated from localStorage on first access,
 *                  synced from Firestore once on sign-in).  Zero Firestore reads
 *                  during a session.
 * Write strategy : only the single changed card is sent to Firestore per answer
 *                  (not the entire document).  localStorage is always written
 *                  synchronously; Firestore is fire-and-forget.
 */

import type { SRSCard, SRSAllData } from './types';
import { applyAnswer, newCard, isDue } from './algorithm';

// ── Lazy Firestore imports (avoids SSR issues) ────────────────────────────────
async function fs() {
  const { doc, getDoc, setDoc } = await import('firebase/firestore');
  const { default: db } = await import('@/lib/firebase/firestore');
  return { db, doc, getDoc, setDoc };
}

// ── In-memory cache ───────────────────────────────────────────────────────────
// Single source of truth during a browser session.
// Initialised lazily from localStorage; overwritten by mergeLocalToFirestore.
let _cache: SRSAllData | null = null;

function getCache(): SRSAllData {
  if (_cache === null) _cache = lsLoad();
  return _cache;
}

function setCache(data: SRSAllData): void {
  _cache = data;
  lsSave(data);
}

// ── localStorage ──────────────────────────────────────────────────────────────
const LS_KEY = 'ws_srs_v1';

function lsLoad(): SRSAllData {
  if (typeof window === 'undefined') return {};
  try { const r = localStorage.getItem(LS_KEY); return r ? JSON.parse(r) : {}; }
  catch { return {}; }
}

function lsSave(data: SRSAllData): void {
  if (typeof window === 'undefined') return;
  try { localStorage.setItem(LS_KEY, JSON.stringify(data)); } catch { /* quota */ }
}

// ── Firestore helpers ─────────────────────────────────────────────────────────
async function fsLoad(uid: string): Promise<SRSAllData> {
  try {
    const { db, doc, getDoc } = await fs();
    const snap = await getDoc(doc(db, 'users', uid, 'srs', 'progress'));
    return snap.exists() ? (snap.data() as SRSAllData) : {};
  } catch { return {}; }
}

/** Write only the single changed card — far cheaper than overwriting the whole doc. */
async function fsSaveCard(uid: string, cardId: string, card: SRSCard): Promise<void> {
  try {
    const { db, doc, setDoc } = await fs();
    await setDoc(doc(db, 'users', uid, 'srs', 'progress'), { [cardId]: card }, { merge: true });
  } catch (e) { console.error('[srs] card save failed', e); }
}

/** Full-document write — only used for the merge-on-login sync. */
async function fsSaveAll(uid: string, data: SRSAllData): Promise<void> {
  try {
    const { db, doc, setDoc } = await fs();
    await setDoc(doc(db, 'users', uid, 'srs', 'progress'), data);
  } catch (e) { console.error('[srs] full save failed', e); }
}

// ── Merge ─────────────────────────────────────────────────────────────────────
function mergeData(local: SRSAllData, remote: SRSAllData): SRSAllData {
  const merged: SRSAllData = { ...remote };
  for (const [id, card] of Object.entries(local)) {
    if (!merged[id] || card.dueDate > merged[id].dueDate) merged[id] = card;
  }
  return merged;
}

// ── Public API ────────────────────────────────────────────────────────────────

/**
 * Called once on sign-in.  Pulls Firestore data, merges with localStorage,
 * writes the merged result back to Firestore, and warms the in-memory cache.
 */
export async function mergeLocalToFirestore(uid: string): Promise<void> {
  const local  = lsLoad();
  const remote = await fsLoad(uid);
  const merged = mergeData(local, remote);
  setCache(merged);                       // warm cache
  if (Object.keys(merged).length > 0) {
    await fsSaveAll(uid, merged);         // one-time full sync
  }
}

/**
 * Record an answer.
 * – Reads from the in-memory cache (no Firestore read).
 * – Writes only the changed card to Firestore (fire-and-forget).
 */
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

  const data     = getCache();
  const existing = data[cardId] ?? newCard(lessonId, section, index);
  const updated  = applyAnswer(existing, quality);
  data[cardId]   = updated;

  setCache(data);                                          // localStorage sync
  if (uid) fsSaveCard(uid, cardId, updated).catch(console.error); // async, no await
}

/** Returns due cards for a lesson — cache only, no Firestore read. */
export async function getDueCards(uid: string | null, lessonId: string): Promise<SRSCard[]> {
  const data = getCache();
  return Object.values(data).filter((c) => c.lessonId === lessonId && isDue(c));
}

/** Returns total due count — cache only, no Firestore read. */
export async function getTotalDueCount(uid: string | null): Promise<number> {
  return Object.values(getCache()).filter(isDue).length;
}

/** Returns all cards seen for a lesson — cache only, no Firestore read. */
export async function getLessonCards(uid: string | null, lessonId: string): Promise<SRSAllData> {
  const result: SRSAllData = {};
  for (const [id, card] of Object.entries(getCache())) {
    if (card.lessonId === lessonId) result[id] = card;
  }
  return result;
}
