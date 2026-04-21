import { MetadataRoute } from 'next';

export const dynamic = 'force-static';

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://sikshya.com';

  // Main pages
  const pages = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'weekly' as const,
      priority: 1,
    },
  ];

  // Quick games
  const quickGames = [
    { url: `${baseUrl}/play/multiplication`, priority: 0.9 },
    { url: `${baseUrl}/play/division`, priority: 0.9 },
  ];

  // Sample lessons (will be expanded with generateStaticParams data in production)
  const lessons = [
    {
      url: `${baseUrl}/class/1/science/living-nonliving`,
      priority: 0.8,
    },
    {
      url: `${baseUrl}/class/1/science/living-nonliving/teach`,
      priority: 0.8,
    },
    {
      url: `${baseUrl}/class/1/science/living-nonliving/practice`,
      priority: 0.8,
    },
    {
      url: `${baseUrl}/class/1/science/living-nonliving/challenge`,
      priority: 0.8,
    },
  ];

  return [
    ...pages,
    ...quickGames.map((game) => ({
      url: game.url,
      lastModified: new Date(),
      changeFrequency: 'monthly' as const,
      priority: game.priority,
    })),
    ...lessons.map((lesson) => ({
      url: lesson.url,
      lastModified: new Date(),
      changeFrequency: 'monthly' as const,
      priority: lesson.priority,
    })),
  ];
}
