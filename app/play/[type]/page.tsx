import { readFileSync } from 'fs';
import { join } from 'path';
import type { LessonData } from '@/lib/engine/types';
import GameLoader from './GameLoader';

export async function generateStaticParams() {
  return [
    { type: 'multiplication' },
    { type: 'division' },
    { type: 'general-addition' },
    { type: 'general-subtraction' },
    { type: 'general-solar-system' },
    { type: 'general-human-body' },
    { type: 'general-animals-world' },
    { type: 'general-spelling-bee' },
    { type: 'general-countries-capitals' },
    { type: 'general-food-nutrition' },
  ];
}

export const metadata = {
  title: 'Play Game - Sikshya',
};

interface PageProps {
  params: Promise<{
    type: string;
  }>;
}

function loadLesson(type: string): LessonData | null {
  try {
    const indexPath = join(process.cwd(), 'data', 'general', 'index.json');
    const index = JSON.parse(readFileSync(indexPath, 'utf-8')) as {
      lessons: Array<{ id: string; file: string }>;
    };
    const gameInfo = index.lessons.find((g) => g.id === type);
    if (!gameInfo) return null;
    const lessonPath = join(process.cwd(), 'data', 'general', `${gameInfo.file}.json`);
    return JSON.parse(readFileSync(lessonPath, 'utf-8')) as LessonData;
  } catch {
    return null;
  }
}

export default async function GamePage({ params }: PageProps) {
  const { type } = await params;
  const initialLesson = loadLesson(type);
  return <GameLoader type={type} initialLesson={initialLesson} />;
}
