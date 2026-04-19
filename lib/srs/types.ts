export interface SRSCard {
  cardId: string;       // e.g. "class-6-math-sets-introduction_practice_3"
  lessonId: string;     // e.g. "class-6-math-sets-introduction"
  section: string;      // "practice" | "challenge"
  index: number;        // item index in that section
  interval: number;     // days until next review
  repetitions: number;  // consecutive correct count
  easeFactor: number;   // SM-2 difficulty (min 1.3, default 2.5)
  dueDate: string;      // ISO date "YYYY-MM-DD"
  lastReviewed: string; // ISO date
}

export type SRSLessonData = Record<string, SRSCard>; // keyed by cardId
export type SRSAllData    = Record<string, SRSCard>; // all cards, any lesson
