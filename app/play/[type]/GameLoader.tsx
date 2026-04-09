'use client';

import dynamic from 'next/dynamic';
import type { LessonData } from '@/lib/engine/types';

// Dynamic import with ssr:false must live in a Client Component
const GameRunnerClient = dynamic(() => import('./GameRunnerClient'), { ssr: false });

interface GameLoaderProps {
  type: string;
  initialLesson: LessonData | null;
}

export default function GameLoader({ type, initialLesson }: GameLoaderProps) {
  return <GameRunnerClient type={type} initialLesson={initialLesson} />;
}
