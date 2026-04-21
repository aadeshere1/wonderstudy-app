import { Metadata } from 'next';

export const siteMetadata: Metadata = {
  title: 'Sikshya - Learn Math, English & Science',
  description:
    'Interactive games for kids to practice and memorize mathematics, English, and science fundamentals. Classes 1-10.',
  keywords: [
    'kids learning',
    'math games',
    'english games',
    'science games',
    'educational games',
    'multiplication',
    'vocabulary',
    'spelling',
  ],
  robots: 'index, follow',
  openGraph: {
    title: 'Sikshya',
    description: 'Interactive educational games for kids',
    type: 'website',
  },
  twitter: {
    card: 'summary',
    title: 'Sikshya',
    description: 'Interactive educational games for kids',
  },
};

export function generateLessonMetadata(
  title: string,
  description: string,
  classNum?: number,
  subject?: string
): Metadata {
  const fullTitle = `${title} - Sikshya`;
  const keywords = [
    title,
    subject || '',
    classNum ? `class ${classNum}` : '',
    'kids learning',
    'educational games',
  ].filter(Boolean);

  return {
    title: fullTitle,
    description,
    keywords,
    openGraph: {
      title: fullTitle,
      description,
      type: 'website',
    },
  };
}

export function generateGameMetadata(
  gameTitle: string,
  description: string
): Metadata {
  const fullTitle = `${gameTitle} - Sikshya`;

  return {
    title: fullTitle,
    description,
    openGraph: {
      title: fullTitle,
      description,
      type: 'website',
    },
  };
}
