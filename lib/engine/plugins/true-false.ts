import {
  TrueFalseQuestion,
  GameConfig,
  GamePlugin,
  LessonData,
  Question,
} from "@/lib/engine/types";

export const trueFalsePlugin: GamePlugin = {
  generateQuestion(lesson, config, usedIndices = []) {
    const section = lesson.practice;
    if (!section || section.gameType !== "true-false") {
      throw new Error("Invalid lesson for true-false plugin");
    }

    const items = section.items as TrueFalseQuestion[];
    if (items.length === 0) {
      throw new Error("No true-false items in lesson");
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
    // True/False always has 2 fixed options
    return ["True", "False"];
  },

  formatQuestion(question) {
    const q = question as TrueFalseQuestion;
    return q.statement;
  },

  async speakQuestion(question, voice) {
    const q = question as TrueFalseQuestion;
    await voice.speak(q.statement);
  },

  checkAnswer(input, question) {
    const q = question as TrueFalseQuestion;
    const userAnswer = input.toLowerCase().trim();
    const correctAnswer = q.answer.toLowerCase();

    return userAnswer === correctAnswer || userAnswer === correctAnswer[0];
  },

  async speakCorrect(question, voice) {
    const cheer = (voice as any).getRandomCheer?.() || "Great!";
    await voice.speak(cheer);
  },

  async speakWrong(question, voice) {
    const q = question as TrueFalseQuestion;
    await voice.speak(`The answer is ${q.answer}`);
  },
};
