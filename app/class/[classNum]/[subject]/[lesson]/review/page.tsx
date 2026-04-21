import { readFileSync } from 'fs';
import { join } from 'path';
import type { LessonData } from '@/lib/engine/types';
import ReviewLoader from './ReviewLoader';

function classFolder(classNum: string) {
  return classNum === 'jlpt' ? 'jlpt' : `class-${classNum}`;
}

function loadLesson(classNum: string, subject: string, lesson: string): LessonData | null {
  try {
    const filePath = join(process.cwd(), 'data', 'classes', classFolder(classNum), subject, `${lesson}.json`);
    return JSON.parse(readFileSync(filePath, 'utf-8')) as LessonData;
  } catch { return null; }
}

export async function generateStaticParams() {
  const { readdirSync, existsSync } = await import('fs');
  const { join } = await import('path');
  const params: { classNum: string; subject: string; lesson: string }[] = [];
  const classesDir = join(process.cwd(), 'data', 'classes');
  if (!existsSync(classesDir)) return params;
  for (const classFolder of readdirSync(classesDir)) {
    const classNum = classFolder.replace('class-', '');
    const classPath = join(classesDir, classFolder);
    for (const subject of readdirSync(classPath)) {
      const subjectPath = join(classPath, subject);
      for (const file of readdirSync(subjectPath)) {
        if (file.endsWith('.json') && file !== 'index.json') {
          params.push({ classNum, subject, lesson: file.replace('.json', '') });
        }
      }
    }
  }
  return params;
}

interface PageProps {
  params: Promise<{ classNum: string; subject: string; lesson: string }>;
}

export default async function ReviewPage({ params }: PageProps) {
  const { classNum, subject, lesson } = await params;
  const lessonData = loadLesson(classNum, subject, lesson);
  return (
    <ReviewLoader
      classNum={classNum}
      subject={subject}
      lesson={lesson}
      initialLesson={lessonData}
    />
  );
}
