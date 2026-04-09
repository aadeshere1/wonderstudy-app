'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { GameEngine } from '@/lib/engine/GameEngine';
import { VoiceManager } from '@/lib/voice/VoiceManager';
import { ConfettiOverlay } from '@/components/layout';
import {
  Timer,
  QuestionDisplay,
  OptionsGrid,
  TypeInput,
  ResultsScreen,
  Podium,
  TableSelector,
} from '@/components/game';
import { LessonData, GameState, ArithmeticConfig } from '@/lib/engine/types';

interface GameRunnerClientProps {
  type: string;
  /** Lesson data pre-loaded by the server component */
  initialLesson: LessonData | null;
}

type Phase = 'loading' | 'select' | 'playing';

export default function GameRunnerClient({ type, initialLesson }: GameRunnerClientProps) {
  const router = useRouter();

  // Lesson comes pre-loaded from server — no client fetch needed
  const lesson = initialLesson;
  const loadError = initialLesson ? null : `Game "${type}" not found`;

  const isArithmetic =
    !!initialLesson &&
    (initialLesson.practice?.gameType === 'arithmetic' ||
      initialLesson.challenge?.gameType === 'arithmetic');

  // Start phase: error → playing (shows error UI), arithmetic → select, other → loading (init engine)
  const [phase, setPhase] = useState<Phase>(
    !initialLesson ? 'playing' : isArithmetic ? 'select' : 'loading'
  );

  // Engine / game state
  const [gameEngine, setGameEngine] = useState<GameEngine | null>(null);
  const [voiceManager, setVoiceManager] = useState<VoiceManager | null>(null);
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [showConfetti, setShowConfetti] = useState(false);

  // ── For non-arithmetic games: init engine immediately on mount ─────────
  useEffect(() => {
    if (phase === 'loading' && lesson && !isArithmetic) {
      initAndStart(lesson, undefined);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ── 2. Init engine + start game ──────────────────────────────────────
  const initAndStart = (lessonData: LessonData, selectedTables: number[] | undefined) => {
    const settings = (() => {
      if (typeof window === 'undefined') return null;
      const saved = localStorage.getItem('wsSettings');
      if (saved) { try { return JSON.parse(saved); } catch { return null; } }
      return null;
    })();

    const defaultSettings = {
      players: [{ name: 'Player 1', active: true, colorIdx: 0 }],
      voiceEngine: 'browser' as const,
      speed: 'normal' as const,
      selectedVoiceURI: '', elVoiceId: '',
      speakQuestion: false, speakAnswer: false, speakCheer: false,
      speakTurn: false, speakTimer: false, speakVerbal: false,
    };
    const finalSettings = settings || defaultSettings;

    // Deep-clone lesson so we can safely patch config
    const patchedLesson: LessonData = JSON.parse(JSON.stringify(lessonData));

    if (selectedTables && selectedTables.length > 0) {
      if (patchedLesson.practice) {
        (patchedLesson.practice.config as ArithmeticConfig).tablesA = selectedTables;
      }
      if (patchedLesson.challenge) {
        (patchedLesson.challenge.config as ArithmeticConfig).tablesA = selectedTables;
      }
    }

    const voice = new VoiceManager(finalSettings.speed);
    setVoiceManager(voice);

    const engine = new GameEngine(patchedLesson, 'practice', finalSettings, voice);
    setGameEngine(engine);

    const handleStateChange = () => setGameState({ ...engine.getState() });
    const handleAnswered = (e: Event) => {
      const event = e as CustomEvent;
      if (event.detail?.correct) {
        setShowConfetti(true);
        setTimeout(() => setShowConfetti(false), 1200);
      }
    };

    engine.addEventListener('question', handleStateChange);
    engine.addEventListener('answered', handleAnswered);
    engine.addEventListener('answered', handleStateChange);
    engine.addEventListener('turn', handleStateChange);
    engine.addEventListener('tick', handleStateChange);
    engine.addEventListener('end', handleStateChange);

    engine.start();
    setPhase('playing');
  };

  // ── Loading ──────────────────────────────────────────────────────────
  if (phase === 'loading') {
    return (
      <div className="fixed inset-0 flex items-center justify-center" style={{ background: '#0d0d1a' }}>
        <div className="text-center">
          <div className="text-6xl mb-4 animate-bounce">⭐</div>
          <div className="font-display text-2xl" style={{ color: '#fbbf24' }}>Loading…</div>
        </div>
      </div>
    );
  }

  // ── Table Selector ───────────────────────────────────────────────────
  if (phase === 'select' && lesson) {
    const operation =
      (lesson.practice?.config as ArithmeticConfig)?.operation ||
      (lesson.challenge?.config as ArithmeticConfig)?.operation ||
      'multiply';

    return (
      <TableSelector
        title={lesson.meta.title}
        icon={lesson.meta.icon || '🔢'}
        description={lesson.meta.description}
        operation={operation}
        onStart={(tables) => initAndStart(lesson, tables)}
        onBack={() => router.back()}
      />
    );
  }

  // ── Error ────────────────────────────────────────────────────────────
  if (loadError || !gameEngine || !gameState || !lesson) {
    const msg = loadError || 'Game failed to load';
    return (
      <div className="fixed inset-0 flex items-center justify-center p-4" style={{ background: '#0d0d1a' }}>
        <div className="text-center max-w-md">
          <div className="text-5xl mb-4">😬</div>
          <div className="font-display text-2xl text-white mb-3">{msg}</div>
          <button
            onClick={() => router.back()}
            style={{ padding: '12px 28px', borderRadius: '14px', background: 'linear-gradient(135deg,#a78bfa,#f87171)', border: 'none', color: 'white', fontFamily: 'var(--font-fredoka-one),cursive', fontSize: '1rem', cursor: 'pointer' }}
          >
            ← Go Back
          </button>
        </div>
      </div>
    );
  }

  const currentPlayer = gameState.players[gameState.currentPlayer];

  // ── Game Over ────────────────────────────────────────────────────────
  if (!gameState.running) {
    return (
      <div className="fixed inset-0 overflow-y-auto" style={{ background: '#0d0d1a' }}>
        {gameState.players.length > 1 ? (
          <div className="min-h-full py-8">
            <Podium
              players={gameState.players.map((p) => ({
                name: p.name, score: p.score, correct: p.correct, wrong: p.wrong, colorIdx: p.colorIdx,
              }))}
            />
          </div>
        ) : (
          <ResultsScreen
            score={currentPlayer?.score || 0}
            correct={currentPlayer?.correct || 0}
            wrong={currentPlayer?.wrong || 0}
            streak={currentPlayer?.streak || 0}
            playerName={currentPlayer?.name}
            playerColor={currentPlayer?.colorIdx?.toString()}
            onRestart={() => {
              // Go back to table selector
              setGameEngine(null);
              setGameState(null);
              setPhase('select');
            }}
            onExit={() => router.push('/')}
          />
        )}
      </div>
    );
  }

  // ── Game In Progress ─────────────────────────────────────────────────
  const q = gameState.currentQuestion as any;
  const displayText = q?.displayText || q?.question || q?.word || q?.statement || '';
  const spokenText  = q?.spokenText || displayText;
  const hasOptions  = q?.options && q.options.length > 0;
  const progressPct = Math.min(100, Math.round(((gameState.questionNumber || 0) / (gameState.totalQuestions || 20)) * 100));

  return (
    <div className="fixed inset-0 flex flex-col overflow-hidden" style={{ background: '#0d0d1a' }}>
      <ConfettiOverlay active={showConfetti} />

      {/* ── Score | Timer | Streak ── */}
      <div className="flex items-center justify-between flex-shrink-0" style={{ background: '#161628', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <div className="text-center px-5 py-2 min-w-[80px]">
          <div className="text-xs uppercase tracking-widest mb-0.5" style={{ color: 'rgba(240,244,255,0.4)' }}>Score</div>
          <div className="font-display text-3xl" style={{ color: '#fbbf24' }}>{currentPlayer?.score || 0}</div>
        </div>

        {gameState.totalTime > 0 ? (
          <Timer
            seconds={gameState.timeLeft}
            totalSeconds={gameState.totalTime}
            isActive={gameState.running}
            onTimeUp={() => gameEngine.endGame('time')}
          />
        ) : (
          <div className="font-display text-sm px-4 py-1 rounded-3xl" style={{ background: 'linear-gradient(135deg,#a78bfa,#f87171)', color: 'white' }}>
            {lesson.meta.title}
          </div>
        )}

        <div className="text-center px-5 py-2 min-w-[80px]">
          <div className="text-xs uppercase tracking-widest mb-0.5" style={{ color: 'rgba(240,244,255,0.4)' }}>Streak</div>
          <div className="font-display text-3xl" style={{ color: '#34d399' }}>
            {(currentPlayer?.streak || 0) > 0 ? `🔥${currentPlayer?.streak}` : '0'}
          </div>
        </div>
      </div>

      {/* ── Progress bar ── */}
      <div className="flex-shrink-0 h-1.5 mx-4 my-1 rounded-full overflow-hidden" style={{ background: 'rgba(255,255,255,0.07)' }}>
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ width: `${progressPct}%`, background: 'linear-gradient(90deg,#a78bfa,#f87171)' }}
        />
      </div>

      {/* ── Player banner ── */}
      {currentPlayer?.name && (
        <div className="flex justify-center py-1 flex-shrink-0">
          <div className="px-5 py-1.5 rounded-3xl font-display text-sm" style={{ background: 'linear-gradient(135deg,#a78bfa,#f87171)', color: 'white' }}>
            {currentPlayer.name} — Go! 🎯
          </div>
        </div>
      )}

      {/* ── Question area ── */}
      <div className="flex-1 flex flex-col items-center justify-center gap-6 px-4 overflow-hidden">
        {gameState.currentQuestion && (
          <>
            <QuestionDisplay
              displayText={displayText}
              spokenText={spokenText}
              onSpeak={() => voiceManager?.speak(spokenText)}
            />

            {hasOptions ? (
              <OptionsGrid
                options={q.options}
                onSelect={(option) => gameEngine.checkAnswer(option)}
                columns={2}
                disabled={gameState.lastAnswerValue !== undefined}
                correctOption={gameState.lastAnswerCorrect ? gameState.lastAnswerValue : undefined}
                wrongOption={gameState.lastAnswerCorrect === false ? gameState.lastAnswerValue : undefined}
              />
            ) : (
              <TypeInput
                onSubmit={(answer) => gameEngine.checkAnswer(answer)}
                hint={q?.hint}
                disabled={gameState.lastAnswerValue !== undefined}
                isCorrect={gameState.lastAnswerCorrect}
                feedback={
                  gameState.lastAnswerCorrect
                    ? '✓ Correct!'
                    : gameState.lastAnswerCorrect === false
                    ? '✗ Try again!'
                    : undefined
                }
              />
            )}
          </>
        )}
      </div>

      {/* ── Bottom bar: change tables + end game ── */}
      <div className="flex-shrink-0 flex items-center justify-center gap-3 py-3">
        <button
          onClick={() => {
            gameEngine.endGame('manual');
            setGameEngine(null);
            setGameState(null);
            setPhase('select');
          }}
          style={{
            padding: '7px 16px', borderRadius: '10px',
            background: 'rgba(167,139,250,0.12)', border: '1px solid rgba(167,139,250,0.3)',
            color: '#a78bfa', fontFamily: 'var(--font-nunito),sans-serif',
            fontWeight: 800, fontSize: '0.8rem', cursor: 'pointer',
          }}
        >
          ← Change Tables
        </button>
        <button
          onClick={() => gameEngine.endGame('manual')}
          style={{
            padding: '7px 16px', borderRadius: '10px',
            background: '#252545', border: '1px solid rgba(255,255,255,0.1)',
            color: 'rgba(240,244,255,0.5)', fontFamily: 'var(--font-nunito),sans-serif',
            fontWeight: 800, fontSize: '0.8rem', cursor: 'pointer',
          }}
        >
          ✕ End Game
        </button>
      </div>
    </div>
  );
}
