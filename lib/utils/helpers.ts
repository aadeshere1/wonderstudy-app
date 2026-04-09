/**
 * Shuffle an array using Fisher-Yates algorithm
 */
export function shuffleArray<T>(array: T[]): T[] {
  const result = [...array];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

/**
 * Generate a random integer between min and max (inclusive)
 */
export function randomInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Pick a random element from an array
 */
export function pickRandom<T>(array: T[]): T {
  return array[Math.floor(Math.random() * array.length)];
}

/**
 * Clamp a number between min and max
 */
export function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

/**
 * Format a date to a readable string
 */
export function formatDate(date: Date): string {
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

/**
 * Create random stars for background
 */
export function createStars(count: number = 90): Array<{
  size: string;
  left: string;
  top: string;
  duration: string;
}> {
  const stars = [];
  for (let i = 0; i < count; i++) {
    const size = randomInt(1, 4);
    const left = Math.random() * 100;
    const top = Math.random() * 100;
    const duration = randomInt(1, 4);

    stars.push({
      size: `${size}px`,
      left: `${left}%`,
      top: `${top}%`,
      duration: `${duration}s`,
    });
  }
  return stars;
}

/**
 * Create confetti particles
 */
export function createConfetti(count: number = 50): Array<{
  left: string;
  delay: string;
  color: string;
}> {
  const particles = [];
  const colors = ["#fbbf24", "#f87171", "#34d399", "#a78bfa", "#60a5fa", "#f472b6"];

  for (let i = 0; i < count; i++) {
    particles.push({
      left: `${Math.random() * 100}%`,
      delay: `${Math.random() * 0.5}s`,
      color: pickRandom(colors),
    });
  }

  return particles;
}
