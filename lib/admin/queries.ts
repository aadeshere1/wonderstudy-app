/**
 * Admin-side Firestore queries.
 * Reads from the `publicProgress` collection which is readable by any
 * authenticated user (per Firestore security rules in firestore.rules).
 */

import { getFirestore, collection, onSnapshot, doc, getDoc } from 'firebase/firestore';
import type { User } from 'firebase/auth';
import app from '@/lib/firebase/config';
import type { StudentSummary, QuestionProgressMap } from './types';

function db() {
  return getFirestore(app);
}

function docToStudentSummary(id: string, raw: Record<string, unknown>): StudentSummary {
  return {
    uid:               id,
    name:              (raw.name              as string)   ?? 'Unknown',
    email:             (raw.email             as string)   ?? '',
    photoURL:          (raw.photoURL          as string)   ?? '',
    lastSeen:          (raw.lastSeen          as string)   ?? '',
    joinedAt:          (raw.joinedAt          as string)   ?? '',
    totalXP:           (raw.totalXP           as number)   ?? 0,
    level:             (raw.level             as number)   ?? 1,
    levelTitle:        (raw.levelTitle        as string)   ?? 'Seedling',
    levelEmoji:        (raw.levelEmoji        as string)   ?? '🌱',
    totalQuestions:    (raw.totalQuestions    as number)   ?? 0,
    totalCorrect:      (raw.totalCorrect      as number)   ?? 0,
    dailyStreak:       (raw.dailyStreak       as number)   ?? 0,
    maxStreak:         (raw.maxStreak         as number)   ?? 0,
    sessionsCompleted: (raw.sessionsCompleted as number)   ?? 0,
    teachSessions:     (raw.teachSessions     as number)   ?? 0,
    reviewSessions:    (raw.reviewSessions    as number)   ?? 0,
    badgesEarned:      (raw.badgesEarned      as string[]) ?? [],
    lessonsVisited:    (raw.lessonsVisited    as string[]) ?? [],
  };
}

/**
 * Subscribe to real-time student list updates.
 * Calls `onData` immediately with the current snapshot, then on every change.
 * Returns an unsubscribe function — call it on component unmount.
 */
export function subscribeToStudents(
  onData: (students: StudentSummary[]) => void,
  onError?: (e: Error) => void,
): () => void {
  return onSnapshot(
    collection(db(), 'publicProgress'),
    (snap) => {
      const students = snap.docs.map((d) =>
        docToStudentSummary(d.id, d.data() as Record<string, unknown>)
      );
      onData(students);
    },
    (err) => {
      console.error('[admin] subscribeToStudents error:', err);
      onError?.(err);
    },
  );
}

/** Per-question accuracy for one student */
export async function getStudentQuestionProgress(uid: string): Promise<QuestionProgressMap> {
  try {
    const ref  = doc(db(), 'publicProgress', uid, 'questions', 'data');
    const snap = await getDoc(ref);
    return snap.exists() ? (snap.data() as QuestionProgressMap) : {};
  } catch (e) {
    console.error('getStudentQuestionProgress failed', e);
    return {};
  }
}

/**
 * Write per-question accuracy to publicProgress/{uid}/questions/data.
 * Must be called with the User object so getIdToken() can be called first.
 */
export async function recordQuestionProgress(
  user: User,
  lessonId: string,
  section: string,
  index: number,
  correct: boolean,
): Promise<void> {
  try {
    await user.getIdToken(); // ensure Firestore auth token is ready
    const { getFirestore: gf, doc, setDoc, increment, arrayUnion } =
      await import('firebase/firestore');
    const { default: firebaseApp } = await import('@/lib/firebase/config');
    const fdb = gf(firebaseApp);
    const cardId = `${lessonId}_${section}_${index}`;
    const now = new Date().toISOString();

    // Atomic increments — no read needed
    await setDoc(
      doc(fdb, 'publicProgress', user.uid, 'questions', 'data'),
      {
        [cardId]: {
          cardId,
          lessonId,
          section,
          index,
          totalAttempts:      increment(1),
          correctAttempts:    increment(correct ? 1 : 0),
          wrongAttempts:      increment(correct ? 0 : 1),
          lastAttemptCorrect: correct,
          lastAttempted:      now,
        },
      },
      { merge: true }
    );

    // Track which lessons the student has visited
    await setDoc(
      doc(fdb, 'publicProgress', user.uid),
      { lessonsVisited: arrayUnion(lessonId) },
      { merge: true }
    );
  } catch (e) {
    console.error('[admin] recordQuestionProgress failed:', e);
  }
}

/**
 * Fetch lesson JSON from the static /classes/ folder so we can display
 * real question text in the admin view.
 * lessonId format: "class-{n}-{subject}-{slug}"
 * e.g. "class-1-science-living-nonliving"
 */
export async function fetchLessonItems(
  lessonId: string,
): Promise<Record<string, { question: string; answer: string; options: string[] }>> {
  try {
    // class-1-science-living-nonliving → class-1 / science / living-nonliving
    const parts    = lessonId.split('-');
    const classNum = parts[1];         // "1"
    const subject  = parts[2];         // "science"
    const slug     = parts.slice(3).join('-'); // "living-nonliving"
    const url      = `/classes/class-${classNum}/${subject}/${slug}.json`;

    const res = await fetch(url);
    if (!res.ok) return {};
    const json = await res.json();

    const result: Record<string, { question: string; answer: string; options: string[] }> = {};

    for (const section of ['practice', 'challenge']) {
      const items: any[] = json[section]?.items ?? [];
      items.forEach((item: any, i: number) => {
        if (item?.question) {
          result[`${lessonId}_${section}_${i}`] = {
            question: item.question,
            answer:   item.answer,
            options:  item.options ?? [],
          };
        }
      });
    }

    return result;
  } catch {
    return {};
  }
}
