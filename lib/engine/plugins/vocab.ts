import {
  VocabQuestion,
  GameConfig,
  GamePlugin,
  LessonData,
  Question,
} from "@/lib/engine/types";
import { shuffleArray, pickRandom } from "@/lib/utils/helpers";

export const vocabPlugin: GamePlugin = {
  generateQuestion(lesson, config, usedIndices = []) {
    const section = lesson.practice;
    if (!section || section.gameType !== "vocab") {
      throw new Error("Invalid lesson for vocab plugin");
    }

    const items = section.items as VocabQuestion[];
    if (items.length === 0) {
      throw new Error("No vocab items in lesson");
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
    const q = question as VocabQuestion;
    if (q.options && q.options.length > 0) {
      return shuffleArray([...q.options]);
    }
    return [q.answer];
  },

  formatQuestion(question) {
    const q = question as VocabQuestion;
    return q.question;
  },

  async speakQuestion(question, voice) {
    const q = question as VocabQuestion;
    await voice.speak(q.question);
  },

  checkAnswer(input, question) {
    const q = question as VocabQuestion;
    return input.toLowerCase().trim() === q.answer.toLowerCase().trim();
  },

  async speakCorrect(question, voice) {
    const cheer = (voice as any).getRandomCheer?.() || "Great!";
    await voice.speak(cheer);
  },

  async speakWrong(question, voice) {
    const q = question as VocabQuestion;
    await voice.speak(`The answer is ${q.answer}`);
  },
};
