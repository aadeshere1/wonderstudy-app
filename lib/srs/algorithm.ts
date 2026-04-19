import { SRSCard } from './types';

/** Quality scores we use (SM-2 scale 0-5) */
export const QUALITY = {
  CORRECT_CLEAN: 5,   // right answer, no hint
  CORRECT_HINT:  3,   // right answer after hint was shown
  WRONG:         1,   // wrong answer
} as const;

function todayISO(): string {
  return new Date().toISOString().split('T')[0];
}

function addDays(days: number): string {
  const d = new Date();
  d.setDate(d.getDate() + days);
  return d.toISOString().split('T')[0];
}

/** Returns a new card with SM-2 applied. Pure function — no side effects. */
export function applyAnswer(card: SRSCard, quality: number): SRSCard {
  let { interval, repetitions, easeFactor } = card;

  if (quality < 3) {
    // Wrong — reset streak
    interval    = 1;
    repetitions = 0;
  } else {
    // Correct — advance
    if (repetitions === 0) {
      interval = 1;
    } else if (repetitions === 1) {
      interval = 6;
    } else {
      interval = Math.round(interval * easeFactor);
    }
    repetitions += 1;
  }

  // Update easeFactor (clamp to min 1.3)
  easeFactor = Math.max(
    1.3,
    easeFactor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
  );

  return {
    ...card,
    interval,
    repetitions,
    easeFactor: Math.round(easeFactor * 1000) / 1000,
    dueDate:    addDays(interval),
    lastReviewed: todayISO(),
  };
}

/** Create a brand-new card (first time seeing it) */
export function newCard(lessonId: string, section: string, index: number): SRSCard {
  const cardId = `${lessonId}_${section}_${index}`;
  return {
    cardId,
    lessonId,
    section,
    index,
    interval:     1,
    repetitions:  0,
    easeFactor:   2.5,
    dueDate:      todayISO(),  // due immediately
    lastReviewed: '',
  };
}

/** Is a card due today or overdue? */
export function isDue(card: SRSCard): boolean {
  return card.dueDate <= todayISO();
}
