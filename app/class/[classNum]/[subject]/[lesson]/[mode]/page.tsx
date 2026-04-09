import dynamic from 'next/dynamic';
import { Metadata } from 'next';
import { fetchLesson } from '@/lib/data/loader';
import { lessonSchema, gameSchema } from '@/components/seo/SchemaMarkup';

const GameRunnerClient = dynamic(() => import('./GameRunnerClient'));

export async function generateStaticParams() {
  const lessons = [
    { classNum: '1', subject: 'science', lesson: 'living-nonliving' },
    { classNum: '1', subject: 'math', lesson: 'addition-subtraction' },
    { classNum: '1', subject: 'english', lesson: 'animals-vocabulary' },
  ];
  const modes = ['teach', 'practice', 'challenge'];

  return lessons.flatMap((lesson) =>
    modes.map((mode) => ({
      ...lesson,
      mode,
    }))
  );
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ classNum: string; subject: string; lesson: string; mode: string }>;
}): Promise<Metadata> {
  const { classNum, subject, lesson, mode } = await params;
  const path = `classes/class-${classNum}/${subject}/${lesson}`;

  let lessonData;
  try {
    lessonData = await fetchLesson(path);
  } catch (error) {
    return {
      title: 'Play Lesson - WonderStudy',
      description: 'Interactive learning game',
    };
  }

  const modeLabel = mode.charAt(0).toUpperCase() + mode.slice(1);
  const title = `${lessonData.meta.title} - ${modeLabel} Mode - WonderStudy`;
  const description = `${modeLabel} mode for "${lessonData.meta.title}" - Class ${classNum} ${subject}`;

  return {
    title,
    description,
    keywords: [
      lessonData.meta.subject,
      `class ${classNum}`,
      `${mode} mode`,
      'educational game',
      'kids learning',
    ],
    openGraph: {
      title,
      description,
      type: 'website',
    },
  };
}

interface PageProps {
  params: Promise<{
    classNum: string;
    subject: string;
    lesson: string;
    mode: string;
  }>;
}

export default async function LessonPage({ params }: PageProps) {
  const { classNum, subject, lesson, mode } = await params;
  const path = `classes/class-${classNum}/${subject}/${lesson}`;

  let lessonData;
  let schemaMarkup = null;

  try {
    lessonData = await fetchLesson(path);
    const modeLabel = mode.charAt(0).toUpperCase() + mode.slice(1);
    schemaMarkup = gameSchema(
      `${lessonData.meta.title} - ${modeLabel} Mode`,
      `${modeLabel} mode for "${lessonData.meta.title}" - Class ${classNum} ${subject}`
    );
  } catch (error) {
    // Continue without schema if lesson fetch fails
  }

  return (
    <>
      {schemaMarkup && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schemaMarkup) }}
        />
      )}
      <GameRunnerClient
        classNum={classNum}
        subject={subject}
        lesson={lesson}
        mode={mode}
      />
    </>
  );
}
