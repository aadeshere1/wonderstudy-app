import {
  SpellingQuestion,
  GameConfig,
  GamePlugin,
  LessonData,
  Question,
} from "@/lib/engine/types";

export const spellingPlugin: GamePlugin = {
  generateQuestion(lesson, config, usedIndices = []) {
    const section = lesson.practice;
    if (!section || section.gameType !== "spelling") {
      throw new Error("Invalid lesson for spelling plugin");
    }

    const items = section.items as SpellingQuestion[];
    if (items.length === 0) {
      throw new Error("No spelling items in lesson");
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

    const item = items[index];
    return {
      ...item,
      displayHint: item.displayHint || item.word,
      spokenHint: item.spokenHint || `${item.word}. Spell it: ${item.word}`,
    } as SpellingQuestion;
  },

  generateOptions(question, lesson, config) {
    // Spelling is a text input, not MCQ
    return [];
  },

  formatQuestion(question) {
    const q = question as SpellingQuestion;
    return q.displayHint;
  },

  async speakQuestion(question, voice) {
    const q = question as SpellingQuestion;
    await voice.speak(q.spokenHint || q.word);
  },

  checkAnswer(input, question) {
    const q = question as SpellingQuestion;
    const gameConfig = (question as any).config || {};
    const caseSensitive = gameConfig.caseSensitive ?? false;

    const userAnswer = caseSensitive ? input : input.toLowerCase();
    const correctAnswer = caseSensitive ? q.word : q.word.toLowerCase();

    return userAnswer.trim() === correctAnswer.trim();
  },

  async speakCorrect(question, voice) {
    const cheer = (voice as any).getRandomCheer?.() || "Great!";
    await voice.speak(cheer);
  },

  async speakWrong(question, voice) {
    const q = question as SpellingQuestion;
    await voice.speak(`The correct spelling is ${q.word}`);
  },
};
