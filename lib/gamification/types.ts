export interface GamificationData {
  totalXP: number;
  totalQuestions: number;
  totalCorrect: number;
  currentStreak: number;      // consecutive correct answers this session
  maxStreak: number;          // all-time best streak
  lastPlayDate: string;       // YYYY-MM-DD for daily streak
  dailyStreak: number;        // consecutive days played
  badgesEarned: string[];     // badge IDs
  sessionsCompleted: number;  // practice/challenge sessions finished
  teachSessions: number;      // teach sessions finished
  reviewSessions: number;     // review sessions finished
}

export interface Badge {
  id: string;
  emoji: string;
  name: string;
  description: string;
  rarity: 'common' | 'rare' | 'epic' | 'legendary';
}

export interface Level {
  level: number;
  title: string;
  emoji: string;
  minXP: number;
  maxXP: number;        // exclusive — next level starts here
  color: string;        // gradient
}

export interface XPEvent {
  amount: number;
  reason: string;
}

export const DEFAULT_GAMIFICATION: GamificationData = {
  totalXP: 0,
  totalQuestions: 0,
  totalCorrect: 0,
  currentStreak: 0,
  maxStreak: 0,
  lastPlayDate: '',
  dailyStreak: 0,
  badgesEarned: [],
  sessionsCompleted: 0,
  teachSessions: 0,
  reviewSessions: 0,
};
