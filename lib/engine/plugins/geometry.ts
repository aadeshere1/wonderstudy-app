'use client';

import type {
  GeometryQuestion,
  GeometryShape,
  GamePlugin,
} from '@/lib/engine/types';
import { shuffleArray } from '@/lib/utils/helpers';

// ── SVG constants ──────────────────────────────────────────────────────────────
const VW = 300;   // viewBox width
const VH = 190;   // viewBox height
const STROKE  = '#6366f1';              // indigo — visible on both light & dark
const FILL    = 'rgba(99,102,241,0.12)';
const TXTST   = 'font-size:12px;font-weight:700;font-family:system-ui,sans-serif;fill:var(--ws-text)';
const DIMST   = 'font-size:11px;font-weight:600;font-family:system-ui,sans-serif;fill:#6366f1';

// Helpers
const n = (v: number) => Math.round(v * 10) / 10;

function svgLine(x1: number, y1: number, x2: number, y2: number, style: string) {
  return `<line x1="${n(x1)}" y1="${n(y1)}" x2="${n(x2)}" y2="${n(y2)}" style="${style}"/>`;
}
function svgText(x: number, y: number, label: string, anchor = 'middle', style = DIMST) {
  return `<text x="${n(x)}" y="${n(y)}" text-anchor="${anchor}" style="${style}">${label}</text>`;
}

/**
 * Draw a dimension line between two points with end ticks and a centred label.
 * The label is placed `offset` pixels away from the line midpoint (perpendicular).
 */
function dimLine(
  x1: number, y1: number,
  x2: number, y2: number,
  label: string,
  labelOffsetX = 0,
  labelOffsetY = -6,
): string {
  const mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
  const dx = x2 - x1, dy = y2 - y1;
  const len = Math.sqrt(dx * dx + dy * dy) || 1;
  // perpendicular unit vector
  const nx = -dy / len * 5, ny = dx / len * 5;
  const lineStyle = `stroke:${STROKE};stroke-width:1.2;stroke-dasharray:3,3;fill:none`;
  const tickStyle = `stroke:${STROKE};stroke-width:1.5;fill:none`;
  return [
    svgLine(x1, y1, x2, y2, lineStyle),
    svgLine(x1 - nx, y1 - ny, x1 + nx, y1 + ny, tickStyle),
    svgLine(x2 - nx, y2 - ny, x2 + nx, y2 + ny, tickStyle),
    svgText(mx + labelOffsetX, my + labelOffsetY, label),
  ].join('\n');
}

/** Small right-angle square marker at corner (cx, cy).
 *  quadrant: 'br' = bottom-right meaning the arms extend right & down */
function rightAngle(cx: number, cy: number, quadrant: 'br' | 'bl' | 'tr' | 'tl', size = 9): string {
  const sx = quadrant.includes('r') ? size : -size;
  const sy = quadrant.includes('b') ? -size : size;
  return `<path d="M ${n(cx + sx)} ${n(cy)} L ${n(cx + sx)} ${n(cy + sy)} L ${n(cx)} ${n(cy + sy)}" fill="none" stroke="${STROKE}" stroke-width="1.5"/>`;
}

/** Equal-length tick mark on a line segment */
function equalTick(mx: number, my: number, angle: number, halfLen = 6): string {
  const cos = Math.cos(angle + Math.PI / 2), sin = Math.sin(angle + Math.PI / 2);
  const x1 = mx - cos * halfLen, y1 = my - sin * halfLen;
  const x2 = mx + cos * halfLen, y2 = my + sin * halfLen;
  return svgLine(x1, y1, x2, y2, `stroke:${STROKE};stroke-width:1.5;fill:none`);
}

// ── Shape SVG generators ───────────────────────────────────────────────────────

function rectangleSVG(shape: GeometryShape): string {
  const { width = 1, height = 1, unit = '' } = shape;
  const PAD = 52;
  const maxW = VW - 2 * PAD, maxH = VH - 2 * PAD;
  const rawAspect = width / height;
  const aspect = Math.min(3.5, Math.max(0.28, rawAspect));
  let rw: number, rh: number;
  if (aspect >= maxW / maxH) { rw = maxW; rh = rw / aspect; }
  else { rh = maxH; rw = rh * aspect; }
  const rx = (VW - rw) / 2, ry = (VH - rh) / 2;

  const DGAP = 18; // gap between shape edge and dimension line
  return `<svg viewBox="0 0 ${VW} ${VH}" xmlns="http://www.w3.org/2000/svg">
  <rect x="${n(rx)}" y="${n(ry)}" width="${n(rw)}" height="${n(rh)}"
    fill="${FILL}" stroke="${STROKE}" stroke-width="2.5" rx="3"/>
  ${dimLine(rx, ry - DGAP, rx + rw, ry - DGAP, `${width} ${unit}`, 0, -8)}
  ${dimLine(rx + rw + DGAP, ry, rx + rw + DGAP, ry + rh, `${height} ${unit}`, 18, 4)}
</svg>`;
}

function squareSVG(shape: GeometryShape): string {
  const { side = 1, unit = '' } = shape;
  const size = Math.min(VW - 90, VH - 50);
  const sx = (VW - size) / 2, sy = (VH - size) / 2;
  const mid = size / 2;
  // Four equal-side ticks (one on each side, at midpoint)
  const ticks = [
    equalTick(sx + mid, sy, 0),           // top
    equalTick(sx + mid, sy + size, 0),    // bottom
    equalTick(sx, sy + mid, Math.PI / 2), // left
    equalTick(sx + size, sy + mid, Math.PI / 2), // right
  ].join('\n');

  return `<svg viewBox="0 0 ${VW} ${VH}" xmlns="http://www.w3.org/2000/svg">
  <rect x="${n(sx)}" y="${n(sy)}" width="${n(size)}" height="${n(size)}"
    fill="${FILL}" stroke="${STROKE}" stroke-width="2.5" rx="3"/>
  ${ticks}
  ${dimLine(sx, sy - 18, sx + size, sy - 18, `${side} ${unit}`, 0, -8)}
</svg>`;
}

function triangleSVG(shape: GeometryShape): string {
  const { unit = '' } = shape;
  const isRight = shape.base !== undefined && shape.triHeight !== undefined;

  if (isRight) {
    // Right-angled at bottom-left
    const { base = 1, triHeight = 1, sideC } = shape;
    const PAD = 50;
    const maxW = VW - 2 * PAD, maxH = VH - 2 * PAD;
    const aspect = Math.min(3.5, Math.max(0.28, base / triHeight));
    let tw: number, th: number;
    if (aspect >= maxW / maxH) { tw = maxW; th = tw / aspect; }
    else { th = maxH; tw = th * aspect; }
    const bx = (VW - tw) / 2, by = (VH + th) / 2; // bottom-left vertex

    const ax = bx, ay = by - th;   // top-left (apex)
    const cx = bx + tw, cy = by;   // bottom-right

    const DGAP = 16;
    return `<svg viewBox="0 0 ${VW} ${VH}" xmlns="http://www.w3.org/2000/svg">
  <polygon points="${n(ax)},${n(ay)} ${n(cx)},${n(cy)} ${n(bx)},${n(by)}"
    fill="${FILL}" stroke="${STROKE}" stroke-width="2.5" stroke-linejoin="round"/>
  ${rightAngle(bx, by, 'br')}
  ${dimLine(bx, by + DGAP, cx, cy + DGAP, `${base} ${unit}`, 0, 12)}
  ${dimLine(ax - DGAP, ay, bx - DGAP, by, `${triHeight} ${unit}`, -20, 4)}
  ${sideC ? svgText((ax + cx) / 2 + 14, (ay + cy) / 2 - 4, `${sideC} ${unit}`) : ''}
</svg>`;
  }

  // General triangle — three sides labeled (for perimeter questions)
  const { sideA = 1, sideB = 1, sideC = 1 } = shape;
  const PAD = 30;
  // Place vertices: bottom-left, bottom-right, top-center
  const ax = PAD, ay = VH - PAD;
  const bx = VW - PAD, by = VH - PAD;
  const cx = VW / 2, cy = PAD + 10;

  return `<svg viewBox="0 0 ${VW} ${VH}" xmlns="http://www.w3.org/2000/svg">
  <polygon points="${ax},${ay} ${bx},${by} ${cx},${cy}"
    fill="${FILL}" stroke="${STROKE}" stroke-width="2.5" stroke-linejoin="round"/>
  ${svgText((ax + bx) / 2, ay + 18, `${sideA} ${unit}`)}
  ${svgText((ax + cx) / 2 - 16, (ay + cy) / 2 + 4, `${sideB} ${unit}`, 'end')}
  ${svgText((bx + cx) / 2 + 16, (by + cy) / 2 + 4, `${sideC} ${unit}`, 'start')}
</svg>`;
}

function circleSVG(shape: GeometryShape): string {
  const { radius = 1, unit = '' } = shape;
  const cr = Math.min((VW - 60) / 2, (VH - 40) / 2);
  const cx = VW / 2, cy = VH / 2;
  return `<svg viewBox="0 0 ${VW} ${VH}" xmlns="http://www.w3.org/2000/svg">
  <circle cx="${cx}" cy="${cy}" r="${n(cr)}"
    fill="${FILL}" stroke="${STROKE}" stroke-width="2.5"/>
  <!-- Centre dot -->
  <circle cx="${cx}" cy="${cy}" r="3" fill="${STROKE}"/>
  <!-- Radius line (dashed) -->
  <line x1="${cx}" y1="${cy}" x2="${n(cx + cr)}" y2="${cy}"
    stroke="${STROKE}" stroke-width="1.8" stroke-dasharray="4,3"/>
  <!-- Radius label -->
  ${svgText(cx + cr / 2, cy - 10, `r = ${radius} ${unit}`)}
</svg>`;
}

/** Generate an inline SVG diagram for a GeometryShape. */
export function generateShapeSVG(shape: GeometryShape): string {
  switch (shape.type) {
    case 'rectangle': return rectangleSVG(shape);
    case 'square':    return squareSVG(shape);
    case 'triangle':  return triangleSVG(shape);
    case 'circle':    return circleSVG(shape);
    default:          return '';
  }
}

// ── Geometry GamePlugin ────────────────────────────────────────────────────────

export const geometryPlugin: GamePlugin = {
  /**
   * Not used by GameEngine for item-list games (engine picks items itself).
   * Kept to satisfy the interface.
   */
  generateQuestion(lesson, _config, _usedIndices = []) {
    const section = lesson.practice;
    const items = (section?.items ?? []) as GeometryQuestion[];
    if (items.length === 0) throw new Error('No geometry items in lesson');
    const item = items[Math.floor(Math.random() * items.length)];
    return { ...item, svg: generateShapeSVG(item.shape) };
  },

  /**
   * Called by GameEngine after each item is picked from the queue.
   * We use this as a hook to:
   *  1. Attach the generated SVG onto the (shallow-copied) question object.
   *  2. Return the shuffled options array.
   */
  generateOptions(question, _lesson, _config) {
    const q = question as GeometryQuestion;
    // Side-effect: stamp the SVG diagram onto the question object so that
    // GameRunnerClient can read q.svg from gameState.currentQuestion.
    if (q.shape && !q.svg) {
      (q as any).svg = generateShapeSVG(q.shape);
    }
    if (!q.options || q.options.length === 0) return [q.answer];
    return shuffleArray([...q.options]);
  },

  formatQuestion(question) {
    return (question as GeometryQuestion).question;
  },

  async speakQuestion(question, voice) {
    await voice.speak((question as GeometryQuestion).question);
  },

  checkAnswer(input, question) {
    const q = question as GeometryQuestion;
    const norm = (s: string) =>
      s.toLowerCase().trim()
        .replace(/\s+/g, ' ')          // collapse whitespace
        .replace(/cm²|cm2/g, 'cm²')   // normalise area units
        .replace(/\s*²/g, '²');
    return norm(input) === norm(q.answer);
  },

  async speakCorrect(_question, voice) {
    const cheer = (voice as any).getRandomCheer?.() ?? 'Excellent!';
    await voice.speak(cheer);
  },

  async speakWrong(question, voice) {
    const q = question as GeometryQuestion;
    await voice.speak(`The answer is ${q.answer}`);
  },
};
