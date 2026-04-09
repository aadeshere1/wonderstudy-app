export interface SchemaMarkupProps {
  schema: Record<string, any>;
}

export const SchemaMarkup = ({ schema }: SchemaMarkupProps) => {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
};

// Organization schema for the site
export const organizationSchema = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'WonderStudy',
  url: 'https://wonderstudy.com',
  description: 'Interactive educational games for kids',
};

// Learning resource schema for lessons
export function lessonSchema(
  title: string,
  description: string,
  classNum?: number,
  subject?: string
) {
  return {
    '@context': 'https://schema.org',
    '@type': 'LearningResource',
    name: title,
    description: description,
    educationalLevel: classNum ? `Grade ${classNum}` : undefined,
    learningResourceType: 'Quiz',
    teaches: subject ? subject.charAt(0).toUpperCase() + subject.slice(1) : undefined,
    interactivityType: 'active',
    isAccessibleForFree: true,
  };
}

// Game/interactive content schema
export function gameSchema(title: string, description: string) {
  return {
    '@context': 'https://schema.org',
    '@type': 'EducationalGameBoard',
    name: title,
    description: description,
    isAccessibleForFree: true,
    inLanguage: 'en',
    author: {
      '@type': 'Organization',
      name: 'WonderStudy',
    },
  };
}

// Breadcrumb schema for navigation
export function breadcrumbSchema(
  items: Array<{ name: string; url: string }>
) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.url,
    })),
  };
}
