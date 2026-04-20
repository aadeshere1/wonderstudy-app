import type { Level } from './types';

export const LEVELS: Level[] = [
  { level: 1, title: 'Seedling',   emoji: '🌱', minXP: 0,     maxXP: 100,   color: 'linear-gradient(135deg,#86efac,#22c55e)' },
  { level: 2, title: 'Sprout',     emoji: '🌿', minXP: 100,   maxXP: 300,   color: 'linear-gradient(135deg,#6ee7b7,#059669)' },
  { level: 3, title: 'Explorer',   emoji: '🔭', minXP: 300,   maxXP: 600,   color: 'linear-gradient(135deg,#67e8f9,#0891b2)' },
  { level: 4, title: 'Scholar',    emoji: '📖', minXP: 600,   maxXP: 1100,  color: 'linear-gradient(135deg,#93c5fd,#2563eb)' },
  { level: 5, title: 'Champion',   emoji: '🔥', minXP: 1100,  maxXP: 2000,  color: 'linear-gradient(135deg,#a78bfa,#7c3aed)' },
  { level: 6, title: 'Prodigy',    emoji: '⚡', minXP: 2000,  maxXP: 3500,  color: 'linear-gradient(135deg,#f9a8d4,#db2777)' },
  { level: 7, title: 'Legend',     emoji: '🏆', minXP: 3500,  maxXP: 6000,  color: 'linear-gradient(135deg,#fbbf24,#f97316)' },
  { level: 8, title: 'Mastermind', emoji: '👑', minXP: 6000,  maxXP: Infinity, color: 'linear-gradient(135deg,#fbbf24,#a78bfa)' },
];

export function getLevelForXP(xp: number): Level {
  for (let i = LEVELS.length - 1; i >= 0; i--) {
    if (xp >= LEVELS[i].minXP) return LEVELS[i];
  }
  return LEVELS[0];
}

export function getXPProgress(xp: number): { current: number; needed: number; pct: number } {
  const lvl = getLevelForXP(xp);
  if (lvl.maxXP === Infinity) return { current: xp - lvl.minXP, needed: 0, pct: 100 };
  const current = xp - lvl.minXP;
  const needed  = lvl.maxXP - lvl.minXP;
  return { current, needed, pct: Math.min(100, Math.round((current / needed) * 100)) };
}

/** Returns true if going from oldXP to newXP crosses a level boundary */
export function didLevelUp(oldXP: number, newXP: number): Level | null {
  const oldLvl = getLevelForXP(oldXP);
  const newLvl = getLevelForXP(newXP);
  return newLvl.level > oldLvl.level ? newLvl : null;
}
