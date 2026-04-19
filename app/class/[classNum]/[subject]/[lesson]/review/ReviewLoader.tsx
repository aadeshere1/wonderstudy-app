'use client';

import dynamic from 'next/dynamic';
import type { LessonData } from '@/lib/engine/types';

const ReviewClient = dynamic(() => import('./ReviewClient'), { ssr: false });

interface Props {
  classNum: string;
  subject: string;
  lesson: string;
  initialLesson: LessonData | null;
}

export default function ReviewLoader(props: Props) {
  return <ReviewClient {...props} />;
}
