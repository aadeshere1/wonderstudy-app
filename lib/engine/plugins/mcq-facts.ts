import {
  MCQFactsQuestion,
  GameConfig,
  GamePlugin,
  LessonData,
  Question,
} from "@/lib/engine/types";
import { shuffleArray } from "@/lib/utils/helpers";

export const mcqFactsPlugin: GamePlugin = {
  generateQuestion(lesson, config, usedIndices = []) {
    const section = lesson.practice;
    if (!section || section.gameType !== "mcq-facts") {
      throw new Error("Invalid lesson for mcq-facts plugin");
    }

    const items = section.items as MCQFactsQuestion[];
    if (items.length === 0) {
      throw new Error("No mcq-facts items in lesson");
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
    const q = question as MCQFactsQuestion;
    const gameConfig = config as any;

    if (!q.options || q.options.length === 0) {
      return [q.answer];
    }

    if (gameConfig.shuffleOptions) {
      return shuffleArray(q.options);
    }
    return q.options;
  },

  formatQuestion(question) {
    const q = question as MCQFactsQuestion;
    return q.question;
  },

  async speakQuestion(question, voice) {
    const q = question as MCQFactsQuestion;
    await voice.speak(q.question);
  },

  checkAnswer(input, question) {
    const q = question as MCQFactsQuestion;
    return input.toLowerCase().trim() === q.answer.toLowerCase().trim();
  },

  async speakCorrect(question, voice) {
    const cheer = (voice as any).getRandomCheer?.() || "Great!";
    await voice.speak(cheer);
  },

  async speakWrong(question, voice) {
    const q = question as MCQFactsQuestion;
    await voice.speak(`The answer is ${q.answer}`);
  },
};
