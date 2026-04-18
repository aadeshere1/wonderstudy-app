'use client';

import dynamic from 'next/dynamic';
import type { LessonData } from '@/lib/engine/types';

const GameRunnerClient = dynamic(() => import('./GameRunnerClient'), { ssr: false });

interface GameLoaderProps {
  classNum: string;
  subject: string;
  lesson: string;
  mode: string;
  initialLesson: LessonData | null;
}

export default function GameLoader(props: GameLoaderProps) {
  return <GameRunnerClient {...props} />;
}
