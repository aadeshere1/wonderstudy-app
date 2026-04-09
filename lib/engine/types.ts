export type GameMode = "teach" | "practice" | "challenge";
export type GameType =
  | "arithmetic"
  | "vocab"
  | "spelling"
  | "mcq-facts"
  | "true-false"
  | "word-meaning";
export type Operation = "multiply" | "divide" | "add" | "subtract" | "mixed";
export type ArithmeticAnswerMode = "quiz" | "type";
export type VocabAnswerMode = "mcq" | "type";
export type Direction = "word-to-meaning" | "meaning-to-word";

// Lesson Metadata
export interface LessonMeta {
  title: string;
  subject: "math" | "english" | "science" | "general";
  class: number | null;
  lesson: string | null;
  subtopic: string;
  description: string;
  icon: string;
  difficulty: "beginner" | "intermediate" | "advanced";
}

// Section Config Interfaces
export interface ArithmeticConfig {
  operation: Operation;
  rangeA: [number, number];
  rangeB: [number, number];
  /** Optional override: pick the first operand (or divisor) from this list */
  tablesA?: number[];
  timeLimit: number;
  questionsCount: number;
  answerMode: ArithmeticAnswerMode;
}

export interface VocabConfig {
  answerMode: VocabAnswerMode;
  optionsCount: number;
  timeLimit: number;
  questionsCount: number;
}

export interface SpellingConfig {
  speakWord: boolean;
  caseSensitive: boolean;
  timeLimit: number;
  questionsCount: number;
}

export interface MCQFactsConfig {
  shuffleOptions: boolean;
  timeLimit: number;
  questionsCount: number;
}

export interface TrueFalseConfig {
  timeLimit: number;
  questionsCount: number;
}

export interface WordMeaningConfig {
  answerMode: "mcq" | "type";
  optionsCount: number;
  direction: Direction;
  timeLimit: number;
  questionsCount: number;
}

export type GameConfig =
  | ArithmeticConfig
  | VocabConfig
  | SpellingConfig
  | MCQFactsConfig
  | TrueFalseConfig
  | WordMeaningConfig;

// Question Items
export interface BaseQuestion {
  hint?: string;
}

export interface ArithmeticQuestion extends BaseQuestion {
  a: number;
  b: number;
  answer: number;
  operation: Operation;
  displayText: string;
  spokenText: string;
}

export interface VocabQuestion extends BaseQuestion {
  question: string;
  answer: string;
  options: string[];
  audio?: string;
  image?: string;
}

export interface SpellingQuestion extends BaseQuestion {
  word: string;
  displayHint: string;
  spokenHint?: string;
  audio?: string;
  image?: string;
}

export interface MCQFactsQuestion extends BaseQuestion {
  question: string;
  answer: string;
  options: string[];
  explanation?: string;
  image?: string;
}

export interface TrueFalseQuestion extends BaseQuestion {
  statement: string;
  answer: "true" | "false";
  explanation?: string;
}

export interface WordMeaningQuestion extends BaseQuestion {
  word: string;
  meaning: string;
  options: string[];
  exampleSentence?: string;
  image?: string;
}

export type Question =
  | ArithmeticQuestion
  | VocabQuestion
  | SpellingQuestion
  | MCQFactsQuestion
  | TrueFalseQuestion
  | WordMeaningQuestion;

// Teach/Practice/Challenge Sections
export interface FlashcardItem {
  front: string;
  back: string;
  hint?: string;
}

export interface TeachSection {
  type: "flashcard";
  items: FlashcardItem[];
}

export interface GameSection {
  gameType: GameType;
  config: GameConfig;
  items: unknown[]; // Can be any question type items, or empty for arithmetic
}

// Full Lesson Data
export interface LessonData {
  id: string;
  meta: LessonMeta;
  teach: TeachSection | null;
  practice: GameSection;
  challenge: GameSection;
}

// Game State
export interface Player {
  name: string;
  active: boolean;
  score: number;
  streak: number;
  correct: number;
  wrong: number;
  colorIdx: number;
}

export interface GameState {
  players: Player[];
  currentPlayer: number;
  currentQuestion: Question | null;
  currentCardIndex: number; // For teach mode
  score: number;
  timeLeft: number;
  totalTime: number;
  questionNumber: number;
  totalQuestions: number;
  running: boolean;
  warnedTen: boolean;
  lastAnswerCorrect?: boolean;
  lastAnswerValue?: string;
}

// Settings
export interface PlayerSettings {
  name: string;
  active: boolean;
}

export interface Settings {
  voiceEngine: "browser" | "elevenlabs";
  selectedVoiceURI: string;
  elVoiceId: string;
  elApiKey?: string;
  speed: "slow" | "normal" | "fast";
  speakQuestion: boolean;
  speakAnswer: boolean;
  speakCheer: boolean;
  speakTurn: boolean;
  speakTimer: boolean;
  speakVerbal: boolean;
  players: PlayerSettings[];
}

// Game Record
export interface GameRecord {
  lessonId: string;
  lessonTitle: string;
  mode: GameMode;
  players: Array<{
    name: string;
    score: number;
    correct: number;
    wrong: number;
  }>;
  score: number;
  duration: number;
  date: string;
  timestamp: number;
}

// Plugin Interface
export interface GamePlugin {
  generateQuestion(
    lessonData: LessonData,
    config: GameConfig,
    usedIndices?: number[]
  ): Question;
  generateOptions(
    question: Question,
    lessonData: LessonData,
    config: GameConfig
  ): string[];
  formatQuestion(question: Question): string;
  speakQuestion(question: Question, voiceManager: any): Promise<void>;
  checkAnswer(input: string, question: Question): boolean;
  speakCorrect(question: Question, voiceManager: any): Promise<void>;
  speakWrong(question: Question, voiceManager: any): Promise<void>;
}

// Lesson Index (for each class/subject folder)
export interface LessonIndexItem {
  id: string;
  file: string;
  title: string;
  icon: string;
  subtopics?: string[];
}

export interface LessonIndex {
  lessons: LessonIndexItem[];
}
