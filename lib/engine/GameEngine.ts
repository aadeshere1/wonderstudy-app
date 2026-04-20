"use client";

import {
  GameMode,
  GameState,
  GameType,
  LessonData,
  Player,
  Question,
  Settings,
} from "@/lib/engine/types";
import { VoiceManager } from "@/lib/voice/VoiceManager";
import {
  arithmeticPlugin,
  mcqFactsPlugin,
  spellingPlugin,
  trueFalsePlugin,
  vocabPlugin,
  wordMeaningPlugin,
} from "@/lib/engine/plugins";
import { shuffleArray } from "@/lib/utils/helpers";

const PLAYER_COLORS = ["#a78bfa", "#f87171", "#34d399", "#fbbf24"];
const QUESTIONS_PER_TURN = 5;

export class GameEngine extends EventTarget {
  private lesson: LessonData;
  private mode: GameMode;
  private settings: Settings;
  private voice: VoiceManager;
  private state: GameState;
  private timerInterval: NodeJS.Timeout | null = null;
  // Pre-shuffled queue of item indices — built once at start(), stepped through
  // sequentially so every question appears exactly once before any repeats.
  private _questionQueue: number[] = [];
  private _queuePos: number = 0;
  private currentItemIndex: number = -1; // tracks which item index is being shown

  constructor(
    lesson: LessonData,
    mode: GameMode,
    settings: Settings,
    voice: VoiceManager
  ) {
    super();
    this.lesson = lesson;
    this.mode = mode;
    this.settings = settings;
    this.voice = voice;

    const activePlayers = settings.players
      .filter((p) => p.active)
      .map((p, i) => ({
        ...p,
        score: 0,
        streak: 0,
        correct: 0,
        wrong: 0,
        colorIdx: i % PLAYER_COLORS.length,
      }));

    this.state = {
      players: activePlayers,
      currentPlayer: 0,
      currentQuestion: null,
      currentCardIndex: 0,
      score: 0,
      timeLeft: 0,
      totalTime: 0,
      questionNumber: 0,
      totalQuestions: 0,
      running: false,
      warnedTen: false,
    };
  }

  /**
   * Start the game
   */
  start(): void {
    const section =
      this.mode === "teach"
        ? this.lesson.teach
        : this.mode === "practice"
          ? this.lesson.practice
          : this.lesson.challenge;

    if (!section) {
      throw new Error(`No ${this.mode} section in lesson`);
    }

    // Initialize total questions
    if (this.mode === "teach" && "type" in section) {
      const teachSection = section as any;
      this.state.totalQuestions = teachSection.items.length;
    } else if (this.mode !== "teach") {
      const gameSection = section as any;
      this.state.totalQuestions = gameSection.config.questionsCount || 20;

      // Set up timer if needed
      if (gameSection.config.timeLimit > 0) {
        this.state.totalTime = gameSection.config.timeLimit;
        this.state.timeLeft = gameSection.config.timeLimit;
        this._startTimer();
      }
    }

    this.state.running = true;

    // Build the shuffled question queue for item-list games (practice/challenge).
    // Dynamic plugins (e.g. arithmetic) have no items — queue stays empty and
    // _generateQuestion falls back to plugin.generateQuestion() instead.
    if (this.mode !== "teach") {
      const gameSection = section as any;
      const items: unknown[] = gameSection.items ?? [];
      if (items.length > 0) {
        this._questionQueue = shuffleArray(items.map((_, i) => i));
        this._queuePos = 0;
      }
    }

    if (this.mode === "teach") {
      this._generateTeachCard();
    } else {
      this._generateQuestion();
    }
  }

  /**
   * Generate the next question (for practice/challenge modes).
   *
   * Picks the next index from the pre-shuffled queue built in start().
   * When the queue is exhausted (all items shown once), it is reshuffled
   * so the session can continue for as many questions as configured.
   */
  private _generateQuestion(): void {
    if (!this.state.running) return;

    const section =
      this.mode === "practice"
        ? this.lesson.practice
        : this.lesson.challenge;

    if (!section || this.mode === "teach") return;

    const plugin = this._getPlugin(section.gameType);
    if (!plugin) throw new Error(`Unknown game type: ${section.gameType}`);

    const items: any[] = (section as any).items ?? [];

    // For untimed modes (practice): end after questionsCount questions.
    // totalTime === 0 means no timer. Skip this check for dynamic plugins
    // (no items) — they manage their own cycling.
    if (
      items.length > 0 &&
      this.state.totalTime === 0 &&
      this.state.questionNumber >= this.state.totalQuestions
    ) {
      this.endGame("completed");
      return;
    }

    let question: any;

    if (items.length === 0) {
      // ── Dynamic plugin (e.g. arithmetic): generate question on the fly ──
      if (!plugin.generateQuestion) {
        throw new Error(`No items and no generateQuestion for ${section.gameType}`);
      }
      question = { ...plugin.generateQuestion(this.lesson, section.config, []) };
      this.currentItemIndex = -1; // no meaningful index for dynamic questions
    } else {
      // ── Item-list plugin: step through pre-shuffled queue ────────────────
      // Reshuffle when every item has been shown once.
      if (this._queuePos >= this._questionQueue.length) {
        this._questionQueue = shuffleArray(items.map((_, i) => i));
        this._queuePos = 0;
      }
      const itemIndex = this._questionQueue[this._queuePos++];
      this.currentItemIndex = itemIndex;
      // Shallow-copy so we don't mutate the original lesson data.
      question = { ...items[itemIndex] };
    }

    // Always shuffle options when the plugin supports it, regardless of answerMode
    // label ("quiz", "mcq", etc.) so the correct answer is never in a fixed position.
    if (plugin.generateOptions) {
      question.options = plugin.generateOptions(question, this.lesson, section.config);
    }

    this.state.currentQuestion = question;
    this.state.questionNumber++;

    // Emit question event
    this.dispatchEvent(
      new CustomEvent("question", {
        detail: {
          question,
          player: this.state.players[this.state.currentPlayer],
          questionNumber: this.state.questionNumber,
          totalQuestions: this.state.totalQuestions,
        },
      })
    );

    // Speak question if enabled
    if (this.settings.speakQuestion) {
      this.voice.speak(this._formatQuestionText(question)).catch(() => {});
    }

    // Emit turn event to sync state
    this.dispatchEvent(
      new CustomEvent("turn", {
        detail: {
          player: this.state.players[this.state.currentPlayer],
          questionNumber: this.state.questionNumber,
        },
      })
    );
  }

  /**
   * Generate the next teach card (flashcard)
   */
  private _generateTeachCard(): void {
    const section = this.lesson.teach;
    if (!section || section.type !== "flashcard") {
      return;
    }

    const items = section.items;
    if (this.state.currentCardIndex >= items.length) {
      this.endGame("completed");
      return;
    }

    const item = items[this.state.currentCardIndex];

    // Emit card event
    this.dispatchEvent(
      new CustomEvent("card", {
        detail: {
          front: item.front,
          back: item.back,
          hint: item.hint,
          index: this.state.currentCardIndex,
          total: items.length,
        },
      })
    );
  }

  /**
   * Check answer for current question
   */
  checkAnswer(input: string): void {
    if (!this.state.running || !this.state.currentQuestion) {
      return;
    }

    const section =
      this.mode === "practice"
        ? this.lesson.practice
        : this.lesson.challenge;

    if (!section || this.mode === "teach") {
      return;
    }

    const plugin = this._getPlugin(section.gameType);
    if (!plugin) return;

    const isCorrect = plugin.checkAnswer(input, this.state.currentQuestion);
    const currentPlayer = this.state.players[this.state.currentPlayer];

    // Resolve the correct answer from the current question
    const correctAnswer =
      this.state.currentQuestion && "answer" in this.state.currentQuestion
        ? String((this.state.currentQuestion as any).answer)
        : undefined;

    // Store feedback in state BEFORE dispatching events so that
    // synchronous event listeners (handleStateChange) see the values.
    this.state.lastAnswerCorrect = isCorrect;
    this.state.lastAnswerValue = input;
    this.state.correctAnswerValue = correctAnswer;

    // Update player stats and emit events
    if (isCorrect) {
      const points = 10 + currentPlayer.streak * 2;
      currentPlayer.score += points;
      currentPlayer.streak++;
      currentPlayer.correct++;
      this.state.score += points;

      // Emit answered event
      this.dispatchEvent(
        new CustomEvent("answered", {
          detail: {
            correct: true,
            points,
            streak: currentPlayer.streak,
            player: currentPlayer,
            questionIndex: this.currentItemIndex,
          },
        })
      );

      // Speak feedback
      if (this.settings.speakAnswer) {
        this.voice.speak(this.voice.getRandomCheer()).catch(() => {});
      }
    } else {
      currentPlayer.streak = 0;
      currentPlayer.wrong++;

      // Emit answered event
      this.dispatchEvent(
        new CustomEvent("answered", {
          detail: {
            correct: false,
            points: 0,
            streak: 0,
            player: currentPlayer,
            questionIndex: this.currentItemIndex,
          },
        })
      );

      // Speak correct answer
      if (this.settings.speakAnswer) {
        const answerText = correctAnswer ?? "";
        this.voice
          .speak(`The answer is ${answerText}`)
          .catch(() => {});
      }
    }

    // When wrong: show correct answer for 1500ms so the student can see it.
    // When correct: move on quickly (600ms).
    const delay = isCorrect ? 600 : 1500;

    setTimeout(() => {
      if (this.state.running) {
        this.state.lastAnswerCorrect = undefined;
        this.state.lastAnswerValue = undefined;
        this.state.correctAnswerValue = undefined;
        this._generateQuestion();
      }
    }, delay);
  }

  /**
   * Navigate to next flashcard
   */
  nextCard(): void {
    if (this.mode !== "teach") return;

    this.state.currentCardIndex++;
    this._generateTeachCard();
  }

  /**
   * Navigate to previous flashcard
   */
  prevCard(): void {
    if (this.mode !== "teach") return;

    if (this.state.currentCardIndex > 0) {
      this.state.currentCardIndex--;
      this._generateTeachCard();
    }
  }

  /**
   * Speak current question
   */
  async speakCurrent(): Promise<void> {
    if (!this.state.currentQuestion) return;

    const section =
      this.mode === "practice"
        ? this.lesson.practice
        : this.lesson.challenge;

    if (!section || this.mode === "teach") {
      return;
    }

    const plugin = this._getPlugin(section.gameType);
    if (!plugin) return;

    try {
      await plugin.speakQuestion(this.state.currentQuestion, this.voice);
    } catch (e) {
      console.error("Failed to speak question:", e);
    }
  }

  /**
   * End the game
   */
  endGame(reason: "time" | "completed" | "manual"): void {
    this.state.running = false;
    this._stopTimer();

    // Emit end event
    this.dispatchEvent(
      new CustomEvent("end", {
        detail: {
          players: this.state.players,
          score: this.state.score,
          reason,
          questionNumber: this.state.questionNumber,
          totalQuestions: this.state.totalQuestions,
        },
      })
    );
  }

  /**
   * Get current game state
   */
  getState(): GameState {
    return this.state;
  }

  /**
   * Private helper to get plugin for a game type
   */
  private _getPlugin(gameType: GameType) {
    const plugins: Record<GameType, any> = {
      arithmetic: arithmeticPlugin,
      vocab: vocabPlugin,
      spelling: spellingPlugin,
      "mcq-facts": mcqFactsPlugin,
      "true-false": trueFalsePlugin,
      "word-meaning": wordMeaningPlugin,
    };

    return plugins[gameType];
  }

  /**
   * Format question text for display
   */
  private _formatQuestionText(question: Question): string {
    if ("displayText" in question) {
      return question.displayText;
    }
    if ("question" in question) {
      return question.question;
    }
    if ("statement" in question) {
      return question.statement;
    }
    if ("word" in question) {
      return question.word;
    }
    return "";
  }

  /**
   * Start timer
   */
  private _startTimer(): void {
    if (!this.timerInterval) {
      this.timerInterval = setInterval(() => {
        this._onTick();
      }, 1000);
    }
  }

  /**
   * Stop timer
   */
  private _stopTimer(): void {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
  }

  /**
   * Timer tick
   */
  private _onTick(): void {
    this.state.timeLeft--;

    // Emit tick event
    this.dispatchEvent(
      new CustomEvent("tick", {
        detail: {
          timeLeft: this.state.timeLeft,
          totalTime: this.state.totalTime,
        },
      })
    );

    // 10 second warning
    if (this.state.timeLeft === 10 && !this.state.warnedTen) {
      this.state.warnedTen = true;
      if (this.settings.speakTimer) {
        this.voice.speak("10 seconds left!").catch(() => {});
      }
    }

    // Time's up
    if (this.state.timeLeft <= 0) {
      this.endGame("time");
    }
  }
}
