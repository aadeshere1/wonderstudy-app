import {
  ArithmeticQuestion,
  GameConfig,
  GamePlugin,
  LessonData,
  Question,
} from "@/lib/engine/types";
import { shuffleArray, randomInt, clamp } from "@/lib/utils/helpers";

const numberToWord = (n: number): string => {
  const words = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
  ];
  return words[n] || n.toString();
};

/** Pick a random value from an explicit list, or fall back to randomInt. */
function pickNumber(tables: number[] | undefined, min: number, max: number): number {
  if (tables && tables.length > 0) {
    return tables[Math.floor(Math.random() * tables.length)];
  }
  return randomInt(min, max);
}

export const arithmeticPlugin: GamePlugin = {
  generateQuestion(lesson, config, usedIndices = []) {
    const gameConfig = config as any;
    const operation = gameConfig.operation || "multiply";
    const [minA, maxA] = gameConfig.rangeA || [1, 12];
    const [minB, maxB] = gameConfig.rangeB || [1, 12];
    const tablesA: number[] | undefined = gameConfig.tablesA;

    let a: number;
    let b: number;
    let answer: number;

    if (operation === "divide") {
      // For division: tablesA controls the divisor (b)
      answer = randomInt(minA, maxA);
      b = pickNumber(tablesA, minB, maxB);
      a = b * answer;
    } else if (operation === "multiply") {
      // For multiplication: tablesA controls the first factor (a)
      a = pickNumber(tablesA, minA, maxA);
      b = randomInt(minB, maxB);
      answer = a * b;
    } else if (operation === "add") {
      a = randomInt(minA, maxA);
      b = randomInt(minB, maxB);
      answer = a + b;
    } else if (operation === "subtract") {
      b = randomInt(minB, maxB);
      a = randomInt(
        Math.max(minA, b),
        Math.max(maxA, b)
      );
      answer = a - b;
    } else {
      // mixed
      const ops = ["multiply", "divide", "add", "subtract"];
      return arithmeticPlugin.generateQuestion(
        lesson,
        { ...config, operation: ops[randomInt(0, 3)] } as any,
        usedIndices
      );
    }

    const opSymbols: Record<string, string> = {
      multiply: "×",
      divide: "÷",
      add: "+",
      subtract: "−",
    };
    const opSymbol = opSymbols[operation] || "?";

    const displayText = `${a} ${opSymbol} ${b}`;
    const aWord = numberToWord(a);
    const bWord = numberToWord(b);
    const answerWord = numberToWord(answer);

    let spokenText = "";
    if (operation === "multiply") {
      spokenText = `What is ${aWord} times ${bWord}?`;
    } else if (operation === "divide") {
      spokenText = `${a} divided by ${b} equals?`;
    } else if (operation === "add") {
      spokenText = `${aWord} plus ${bWord}?`;
    } else {
      spokenText = `${aWord} minus ${bWord}?`;
    }

    return {
      a,
      b,
      answer,
      operation,
      displayText,
      spokenText,
    } as ArithmeticQuestion;
  },

  generateOptions(question) {
    const q = question as ArithmeticQuestion;
    const correct = q.answer;

    const options = new Set<number>([correct]);

    // Generate 3 wrong answers near the correct one
    while (options.size < 4) {
      const offset = randomInt(-9, 9);
      const wrong = clamp(correct + offset, 0, 144);
      if (wrong !== correct) {
        options.add(wrong);
      }
    }

    return shuffleArray(Array.from(options).map((n) => n.toString()));
  },

  formatQuestion(question) {
    const q = question as ArithmeticQuestion;
    return q.displayText;
  },

  async speakQuestion(question, voice) {
    const q = question as ArithmeticQuestion;
    await voice.speak(q.spokenText);
  },

  checkAnswer(input, question) {
    const q = question as ArithmeticQuestion;
    const userAnswer = parseInt(input, 10);
    return userAnswer === q.answer;
  },

  async speakCorrect(question, voice) {
    const cheer = (voice as any).getRandomCheer?.() || "Great!";
    await voice.speak(cheer);
  },

  async speakWrong(question, voice) {
    const q = question as ArithmeticQuestion;
    await voice.speak(`The answer is ${q.answer}`);
  },
};
