import {
  WordMeaningQuestion,
  GameConfig,
  GamePlugin,
  LessonData,
  Question,
} from "@/lib/engine/types";
import { shuffleArray } from "@/lib/utils/helpers";

export const wordMeaningPlugin: GamePlugin = {
  generateQuestion(lesson, config, usedIndices = []) {
    const section = lesson.practice;
    if (!section || section.gameType !== "word-meaning") {
      throw new Error("Invalid lesson for word-meaning plugin");
    }

    const items = section.items as WordMeaningQuestion[];
    if (items.length === 0) {
      throw new Error("No word-meaning items in lesson");
    }

    let index: number;
    if (usedIndices.length < items.length) {
      do {
        index = Math.floor(Math.random() * items.length);
      } while (usedIndices.includes(index));
      usedIndices.push(index);
    } else {
      index = Math.floor(Math.random() * items.length);
    }

    return items[index];
  },

  generateOptions(question, lesson, config) {
    const q = question as WordMeaningQuestion;
    const gameConfig = config as any;

    if (!q.options || q.options.length === 0) {
      return [q.meaning];
    }

    // Shuffle options
    return shuffleArray(q.options);
  },

  formatQuestion(question) {
    const q = question as WordMeaningQuestion;
    // Could display word or meaning depending on direction
    return q.word;
  },

  async speakQuestion(question, voice) {
    const q = question as WordMeaningQuestion;
    await voice.speak(`What does ${q.word} mean?`);
  },

  checkAnswer(input, question) {
    const q = question as WordMeaningQuestion;
    return input.toLowerCase().trim() === q.meaning.toLowerCase().trim();
  },

  async speakCorrect(question, voice) {
    const cheer = (voice as any).getRandomCheer?.() || "Great!";
    await voice.speak(cheer);
  },

  async speakWrong(question, voice) {
    const q = question as WordMeaningQuestion;
    await voice.speak(`${q.word} means ${q.meaning}`);
  },
};
