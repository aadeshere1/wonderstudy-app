import type { Badge, GamificationData } from './types';

export const ALL_BADGES: Badge[] = [
  // ── First steps ───────────────────────────────────────────────────────────
  { id: 'first_answer',  emoji: '🎯', name: 'First Step',      description: 'Answer your first question',             rarity: 'common'    },
  { id: 'first_correct', emoji: '✅', name: 'Nailed It!',       description: 'Get your first correct answer',          rarity: 'common'    },

  // ── Streaks (questions in a row) ─────────────────────────────────────────
  { id: 'streak_5',   emoji: '🔥', name: 'On Fire!',       description: '5 correct answers in a row',   rarity: 'common'   },
  { id: 'streak_10',  emoji: '💥', name: 'Unstoppable!',   description: '10 correct in a row',          rarity: 'rare'     },
  { id: 'streak_25',  emoji: '⚡', name: 'Lightning Rod',  description: '25 correct in a row',          rarity: 'epic'     },
  { id: 'streak_50',  emoji: '🌪️', name: 'Tornado',        description: '50 correct in a row',          rarity: 'legendary'},

  // ── Total questions answered ──────────────────────────────────────────────
  { id: 'q_10',   emoji: '🎮', name: 'Getting Started', description: 'Answer 10 questions',    rarity: 'common'    },
  { id: 'q_50',   emoji: '📚', name: 'Bookworm',        description: 'Answer 50 questions',    rarity: 'common'    },
  { id: 'q_100',  emoji: '🏅', name: 'Century Club',    description: 'Answer 100 questions',   rarity: 'rare'      },
  { id: 'q_500',  emoji: '🎓', name: 'Scholar',         description: 'Answer 500 questions',   rarity: 'epic'      },
  { id: 'q_1000', emoji: '🧠', name: 'Brainiac',        description: 'Answer 1000 questions',  rarity: 'legendary' },

  // ── Correct answers total ─────────────────────────────────────────────────
  { id: 'correct_10',  emoji: '⭐', name: 'Star Pupil',    description: '10 correct answers total',   rarity: 'common'  },
  { id: 'correct_100', emoji: '🌟', name: 'Superstar',     description: '100 correct answers total',  rarity: 'rare'    },
  { id: 'correct_500', emoji: '💫', name: 'Shooting Star', description: '500 correct answers total',  rarity: 'epic'    },

  // ── Sessions ──────────────────────────────────────────────────────────────
  { id: 'session_1',   emoji: '🎉', name: 'First Session', description: 'Complete your first session',       rarity: 'common' },
  { id: 'session_10',  emoji: '🏋️', name: 'Committed',     description: 'Complete 10 sessions',             rarity: 'rare'   },
  { id: 'teach_1',     emoji: '📖', name: 'Student',       description: 'Complete a Teach session',          rarity: 'common' },
  { id: 'review_1',    emoji: '🔁', name: 'Reviewer',      description: 'Complete a Review session',         rarity: 'common' },

  // ── Daily streaks ─────────────────────────────────────────────────────────
  { id: 'daily_2',  emoji: '📅', name: 'Back Again!',    description: 'Play 2 days in a row',  rarity: 'common'    },
  { id: 'daily_7',  emoji: '🗓️', name: 'Week Warrior',   description: 'Play 7 days in a row',  rarity: 'rare'      },
  { id: 'daily_30', emoji: '🏆', name: 'Month Master',   description: 'Play 30 days in a row', rarity: 'legendary' },

  // ── Levels ────────────────────────────────────────────────────────────────
  { id: 'level_3', emoji: '🌸', name: 'Growing Up',    description: 'Reach Level 3 Explorer',    rarity: 'common' },
  { id: 'level_5', emoji: '🔥', name: 'Champion!',     description: 'Reach Level 5 Champion',    rarity: 'rare'   },
  { id: 'level_8', emoji: '👑', name: 'Mastermind!',   description: 'Reach Level 8 Mastermind',  rarity: 'legendary' },
];

export const BADGE_MAP = Object.fromEntries(ALL_BADGES.map(b => [b.id, b]));

/** Returns array of newly unlocked badge IDs given old vs new data */
export function checkNewBadges(
  prev: GamificationData,
  next: GamificationData,
  newLevel: number,
): string[] {
  const already = new Set(prev.badgesEarned);
  const earned: string[] = [];

  const check = (id: string) => {
    if (!already.has(id)) earned.push(id);
  };

  if (next.totalQuestions >= 1)   check('first_answer');
  if (next.totalCorrect >= 1)     check('first_correct');

  if (next.currentStreak >= 5)    check('streak_5');
  if (next.currentStreak >= 10)   check('streak_10');
  if (next.currentStreak >= 25)   check('streak_25');
  if (next.currentStreak >= 50)   check('streak_50');

  if (next.totalQuestions >= 10)  check('q_10');
  if (next.totalQuestions >= 50)  check('q_50');
  if (next.totalQuestions >= 100) check('q_100');
  if (next.totalQuestions >= 500) check('q_500');
  if (next.totalQuestions >= 1000)check('q_1000');

  if (next.totalCorrect >= 10)    check('correct_10');
  if (next.totalCorrect >= 100)   check('correct_100');
  if (next.totalCorrect >= 500)   check('correct_500');

  if (next.sessionsCompleted >= 1)  check('session_1');
  if (next.sessionsCompleted >= 10) check('session_10');
  if (next.teachSessions >= 1)      check('teach_1');
  if (next.reviewSessions >= 1)     check('review_1');

  if (next.dailyStreak >= 2)  check('daily_2');
  if (next.dailyStreak >= 7)  check('daily_7');
  if (next.dailyStreak >= 30) check('daily_30');

  if (newLevel >= 3) check('level_3');
  if (newLevel >= 5) check('level_5');
  if (newLevel >= 8) check('level_8');

  return earned;
}

export const RARITY_COLORS = {
  common:    { bg: 'rgba(52,211,153,0.15)',  border: 'rgba(52,211,153,0.4)',  text: '#34d399' },
  rare:      { bg: 'rgba(96,165,250,0.15)',  border: 'rgba(96,165,250,0.4)',  text: '#60a5fa' },
  epic:      { bg: 'rgba(167,139,250,0.15)', border: 'rgba(167,139,250,0.4)', text: '#a78bfa' },
  legendary: { bg: 'rgba(251,191,36,0.15)',  border: 'rgba(251,191,36,0.4)',  text: '#fbbf24' },
};
