import { LessonData, LessonIndex } from "@/lib/engine/types";

/**
 * Fetch a lesson JSON file from the data directory
 * @param lessonPath - Path relative to /data (e.g. "general/multiplication" or "classes/class-1/science/living-nonliving")
 */
export async function fetchLesson(lessonPath: string): Promise<LessonData> {
  // Use filesystem access in Node.js environments (server-side)
  if (typeof window === "undefined") {
    try {
      const { readFileSync } = await import("fs");
      const { join } = await import("path");
      const filePath = join(process.cwd(), "data", `${lessonPath}.json`);
      const data = readFileSync(filePath, "utf-8");
      return JSON.parse(data);
    } catch (error) {
      throw new Error(`Failed to load lesson: ${lessonPath}`);
    }
  }

  // Fallback to fetch for browser environments
  const filePath = `/${lessonPath}.json`;
  const response = await fetch(filePath);

  if (!response.ok) {
    throw new Error(`Failed to load lesson: ${lessonPath}`);
  }

  return response.json();
}

/**
 * Get lesson index for a class/subject combination
 * @param classNum - Class number (1-10)
 * @param subject - Subject name (math, english, science)
 */
export async function getLessonIndex(
  classNum: number,
  subject: string
): Promise<LessonIndex> {
  // Use filesystem access in Node.js environments (server-side)
  if (typeof window === "undefined") {
    try {
      const { readFileSync } = await import("fs");
      const { join } = await import("path");
      const filePath = join(
        process.cwd(),
        "data",
        `classes/class-${classNum}/${subject}/index.json`
      );
      const data = readFileSync(filePath, "utf-8");
      return JSON.parse(data);
    } catch (error) {
      return { lessons: [] };
    }
  }

  // Fallback to fetch for browser environments
  const filePath = `/classes/class-${classNum}/${subject}/index.json`;
  const response = await fetch(filePath);

  if (!response.ok) {
    return { lessons: [] };
  }

  return response.json();
}

/**
 * Get all available lessons for a class across all subjects
 */
export async function getClassLessons(classNum: number) {
  const subjects = ["math", "english", "science"];
  const allLessons: Record<string, any> = {};

  for (const subject of subjects) {
    try {
      const index = await getLessonIndex(classNum, subject);
      allLessons[subject] = index.lessons;
    } catch (e) {
      allLessons[subject] = [];
    }
  }

  return allLessons;
}

/**
 * Get all available general games
 */
export async function getGeneralGames(): Promise<LessonIndex> {
  // Use filesystem access in Node.js environments (server-side)
  if (typeof window === "undefined") {
    try {
      const { readFileSync } = await import("fs");
      const { join } = await import("path");
      const filePath = join(process.cwd(), "data", "general/index.json");
      const data = readFileSync(filePath, "utf-8");
      return JSON.parse(data);
    } catch (error) {
      // Default general games if index doesn't exist
      return {
        lessons: [
          {
            id: "multiplication",
            file: "multiplication",
            title: "Multiplication",
            icon: "✖️",
          },
          {
            id: "division",
            file: "division",
            title: "Division",
            icon: "÷",
          },
        ],
      };
    }
  }

  // Fallback to fetch for browser environments
  const response = await fetch("/general/index.json");

  if (!response.ok) {
    // Default general games if index doesn't exist
    return {
      lessons: [
        {
          id: "multiplication",
          file: "multiplication",
          title: "Multiplication",
          icon: "✖️",
        },
        {
          id: "division",
          file: "division",
          title: "Division",
          icon: "÷",
        },
      ],
    };
  }

  return response.json();
}

/**
 * Save a game record to localStorage
 */
export function saveGameRecord(record: any): void {
  try {
    const existing = JSON.parse(
      sessionStorage.getItem("wsRecords") || "[]"
    );
    existing.unshift(record);
    // Keep last 100 records
    const trimmed = existing.slice(0, 100);
    sessionStorage.setItem("wsRecords", JSON.stringify(trimmed));
  } catch (e) {
    console.error("Failed to save game record:", e);
  }
}

/**
 * Get all game records from localStorage
 */
export function getGameRecords(): any[] {
  try {
    return JSON.parse(sessionStorage.getItem("wsRecords") || "[]");
  } catch (e) {
    console.error("Failed to load game records:", e);
    return [];
  }
}

/**
 * Clear all game records
 */
export function clearGameRecords(): void {
  sessionStorage.removeItem("wsRecords");
}
