'use client';

import { createContext, useContext, useEffect, useState, useCallback, useRef } from 'react';
import type { User } from 'firebase/auth';
import { useAuth } from '@/contexts/AuthContext';
import type { GamificationData, Level } from '@/lib/gamification/types';
import { DEFAULT_GAMIFICATION } from '@/lib/gamification/types';
import {
  loadGamification,
  recordGamificationAnswer,
  recordSessionComplete,
  mergeLocalGamificationToFirestore,
  flushGamificationSave,
} from '@/lib/gamification/store';
import type { RecordAnswerResult } from '@/lib/gamification/store';
import { BADGE_MAP } from '@/lib/gamification/badges';
import { getLevelForXP } from '@/lib/gamification/levels';
import type { Badge } from '@/lib/gamification/types';

/**
 * Write gamification summary to publicProgress/{uid} so the admin dashboard
 * can read it. Runs with a fresh ID token to avoid permission race conditions.
 */
async function syncPublicStats(user: User, data: GamificationData): Promise<void> {
  try {
    await user.getIdToken(); // ensure Firestore has a valid token
    const { getFirestore, doc, setDoc } = await import('firebase/firestore');
    const { default: app } = await import('@/lib/firebase/config');
    const db  = getFirestore(app);
    const ref = doc(db, 'publicProgress', user.uid);
    const lvl = getLevelForXP(data.totalXP);
    await setDoc(ref, {
      totalXP:           data.totalXP,
      level:             lvl.level,
      levelTitle:        lvl.title,
      levelEmoji:        lvl.emoji,
      totalQuestions:    data.totalQuestions,
      totalCorrect:      data.totalCorrect,
      dailyStreak:       data.dailyStreak,
      maxStreak:         data.maxStreak,
      badgesEarned:      data.badgesEarned,
      sessionsCompleted: data.sessionsCompleted,
      teachSessions:     data.teachSessions,
      reviewSessions:    data.reviewSessions,
    }, { merge: true });
  } catch (e) {
    console.error('[admin] publicProgress stats sync failed:', e);
  }
}

interface GamificationContextValue {
  data: GamificationData;
  // Called after each question answered in game modes
  onAnswer: (
    correct: boolean,
    mode: 'practice' | 'challenge' | 'review',
    currentStreak: number
  ) => Promise<RecordAnswerResult | null>;
  // Called when a full session ends
  onSessionEnd: (type: 'practice' | 'challenge' | 'teach' | 'review') => Promise<void>;
  // Queue of badges to toast (consumed by BadgeToast)
  pendingBadges: Badge[];
  clearBadge: (id: string) => void;
  // Level-up info to show modal
  pendingLevelUp: Level | null;
  clearLevelUp: () => void;
  // Latest XP gained (for floating +XP animation)
  lastXP: number;
}

const GamificationContext = createContext<GamificationContextValue>({
  data: DEFAULT_GAMIFICATION,
  onAnswer: async () => null,
  onSessionEnd: async () => {},
  pendingBadges: [],
  clearBadge: () => {},
  pendingLevelUp: null,
  clearLevelUp: () => {},
  lastXP: 0,
});

export function GamificationProvider({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  const [data, setData] = useState<GamificationData>(DEFAULT_GAMIFICATION);
  const [pendingBadges, setPendingBadges] = useState<Badge[]>([]);
  const [pendingLevelUp, setPendingLevelUp] = useState<Level | null>(null);
  const [lastXP, setLastXP] = useState(0);
  const prevUid = useRef<string | null>(null);

  // Always-current ref — lets callbacks read latest data without stale closures
  // and without needing to re-create the callback on every answer.
  const dataRef = useRef<GamificationData>(DEFAULT_GAMIFICATION);

  // Keep dataRef in sync whenever state updates
  const setDataAndRef = useCallback((d: GamificationData) => {
    dataRef.current = d;
    setData(d);
  }, []);

  // Load data on auth change
  useEffect(() => {
    const uid = user?.uid ?? null;
    if (uid && prevUid.current === null) {
      // Just signed in — merge local data first
      mergeLocalGamificationToFirestore(uid).catch(console.error);
    }
    prevUid.current = uid;
    loadGamification(uid).then(setDataAndRef).catch(console.error);
  }, [user, setDataAndRef]);

  const onAnswer = useCallback(async (
    correct: boolean,
    mode: 'practice' | 'challenge' | 'review',
    currentStreak: number,
  ): Promise<RecordAnswerResult | null> => {
    try {
      // Pass current in-memory data as `prev` — eliminates the Firestore getDoc
      const result = await recordGamificationAnswer(
        user?.uid ?? null,
        correct,
        mode,
        currentStreak,
        dataRef.current,
      );
      setDataAndRef(result.data);
      setLastXP(result.xpGained);

      // Queue new badges
      if (result.newBadges.length > 0) {
        const badges = result.newBadges
          .map(id => BADGE_MAP[id])
          .filter(Boolean);
        setPendingBadges(prev => [...prev, ...badges]);
      }

      // Queue level up
      if (result.leveledUp) {
        setPendingLevelUp(result.leveledUp);
      }

      // Sync stats to publicProgress for admin dashboard (every 5 answers to reduce writes)
      if (user && result.data.totalQuestions % 5 === 0) {
        syncPublicStats(user, result.data).catch(console.error);
      }

      return result;
    } catch (e) {
      console.error('gamification error', e);
      return null;
    }
  }, [user, setDataAndRef]);

  const onSessionEnd = useCallback(async (type: 'practice' | 'challenge' | 'teach' | 'review') => {
    try {
      // Pass current in-memory data as `prev` — eliminates the Firestore getDoc.
      // recordSessionComplete internally flushes the debounce before its own write.
      const result = await recordSessionComplete(
        user?.uid ?? null,
        type,
        dataRef.current,
      );
      setDataAndRef(result.data);

      if (result.newBadges.length > 0) {
        const badges = result.newBadges.map(id => BADGE_MAP[id]).filter(Boolean);
        setPendingBadges(prev => [...prev, ...badges]);
      }
      if (result.leveledUp) setPendingLevelUp(result.leveledUp);

      // Always sync at session end so admin sees final counts
      if (user) {
        syncPublicStats(user, result.data).catch(console.error);
      }
    } catch (e) {
      console.error('gamification session error', e);
    }
  }, [user, setDataAndRef]);

  const clearBadge = useCallback((id: string) => {
    setPendingBadges(prev => prev.filter(b => b.id !== id));
  }, []);

  const clearLevelUp = useCallback(() => setPendingLevelUp(null), []);

  return (
    <GamificationContext.Provider value={{
      data, onAnswer, onSessionEnd,
      pendingBadges, clearBadge,
      pendingLevelUp, clearLevelUp,
      lastXP,
    }}>
      {children}
    </GamificationContext.Provider>
  );
}

export const useGamification = () => useContext(GamificationContext);
