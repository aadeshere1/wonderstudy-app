export interface StudentProfile {
  uid: string;
  name: string;
  email: string;
  photoURL: string;
  lastSeen: string;   // ISO timestamp
  joinedAt: string;   // ISO timestamp
}

/** Per-question accuracy tracking, stored in publicProgress/{uid}/questions/data */
export interface QuestionProgress {
  cardId: string;         // e.g. "class-1-science-living-nonliving_practice_2"
  lessonId: string;
  section: string;        // "practice" | "challenge" | "review"
  index: number;
  totalAttempts: number;
  correctAttempts: number;
  wrongAttempts: number;
  lastAttemptCorrect: boolean;
  lastAttempted: string;  // ISO timestamp
}

export type QuestionProgressMap = Record<string, QuestionProgress>;

/** Everything needed to render a student card in the admin list */
export interface StudentSummary {
  uid: string;
  name: string;
  email: string;
  photoURL: string;
  lastSeen: string;
  joinedAt: string;
  totalXP: number;
  level: number;
  levelTitle: string;
  levelEmoji: string;
  totalQuestions: number;
  totalCorrect: number;
  dailyStreak: number;
  maxStreak: number;
  sessionsCompleted: number;
  teachSessions: number;
  reviewSessions: number;
  badgesEarned: string[];
  lessonsVisited: string[];
}
