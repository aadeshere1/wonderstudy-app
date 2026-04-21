'use client';

import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { GameEngine } from '@/lib/engine/GameEngine';
import { VoiceManager } from '@/lib/voice/VoiceManager';
import { ConfettiOverlay } from '@/components/layout';
import {
  Timer,
  QuestionDisplay,
  OptionsGrid,
  Flashcard,
  ResultsScreen,
  Podium,
} from '@/components/game';
import { LessonData, GameMode, GameState } from '@/lib/engine/types';
import { useAuth } from '@/contexts/AuthContext';
import { recordAnswer } from '@/lib/srs/store';
import { recordQuestionProgress } from '@/lib/admin/queries';
import { useGamification } from '@/contexts/GamificationContext';

interface GameRunnerClientProps {
  classNum: string;
  subject: string;
  lesson: string;
  mode: string;
  initialLesson: LessonData | null;
}

// Duration options: label + seconds
const DURATION_OPTIONS = [
  { label: '1:30', sublabel: 'Quick', seconds: 90 },
  { label: '5 min', sublabel: 'Warm-up', seconds: 300 },
  { label: '10 min', sublabel: 'Short', seconds: 600 },
  { label: '15 min', sublabel: 'Standard', seconds: 900 },
  { label: '20 min', sublabel: 'Focused', seconds: 1200 },
  { label: '25 min', sublabel: 'Pomodoro', seconds: 1500 },
  { label: '30 min', sublabel: 'Deep dive', seconds: 1800 },
  { label: '35 min', sublabel: 'Extended', seconds: 2100 },
  { label: '40 min', sublabel: 'Marathon', seconds: 2400 },
];

export default function GameRunnerClient({
  classNum,
  subject,
  lesson,
  mode,
  initialLesson,
}: GameRunnerClientProps) {
  const router = useRouter();
  const { user } = useAuth();
  const { onAnswer: gamOnAnswer, onSessionEnd } = useGamification();

  // For challenge mode: null = show picker, number = duration chosen (in seconds)
  const [selectedDuration, setSelectedDuration] = useState<number | null>(
    mode === 'challenge' ? null : 90
  );

  const [gameEngine, setGameEngine] = useState<GameEngine | null>(null);
  const [voiceManager, setVoiceManager] = useState<VoiceManager | null>(null);
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [loading, setLoading] = useState(mode !== 'challenge'); // don't show loader during picker
  const [error, setError] = useState<string | null>(null);
  const [showConfetti, setShowConfetti] = useState(false);

  // Guard: only fire onSessionEnd once per game session
  const sessionEndedRef = useRef(false);

  useEffect(() => {
    // Challenge mode: wait for duration selection
    if (mode === 'challenge' && selectedDuration === null) return;

    if (!initialLesson) {
      setError(`Lesson not found: ${lesson}`);
      setLoading(false);
      return;
    }

    setLoading(true);

    try {
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
        selectedVoiceURI: '',
        elVoiceId: '',
        speakQuestion: false,
        speakAnswer: false,
        speakCheer: false,
        speakTurn: false,
        speakTimer: false,
        speakVerbal: false,
      };

      const finalSettings = settings || defaultSettings;
      const voice = new VoiceManager(finalSettings.speed);
      setVoiceManager(voice);

      // Override challenge timeLimit with user-selected duration
      const lessonForEngine: LessonData =
        mode === 'challenge' && selectedDuration !== null && initialLesson.challenge
          ? {
              ...initialLesson,
              challenge: {
                ...initialLesson.challenge,
                config: {
                  ...(initialLesson.challenge as any).config,
                  timeLimit: selectedDuration,
                },
              },
            }
          : initialLesson;

      const engine = new GameEngine(lessonForEngine, mode as GameMode, finalSettings, voice);
      sessionEndedRef.current = false; // reset guard for new session
      setGameEngine(engine);

      const handleStateChange = () => setGameState({ ...engine.getState() });
      const handleAnswered = (e: Event) => {
        const event = e as CustomEvent;
        const { correct, questionIndex, hintUsed } = event.detail ?? {};
        if (correct) {
          setShowConfetti(true);
          setTimeout(() => setShowConfetti(false), 1200);
        }
        // Record into SRS for practice and challenge modes
        if (mode === 'practice' || mode === 'challenge') {
          const lessonId = initialLesson.id;
          const section  = mode;
          const index    = typeof questionIndex === 'number' ? questionIndex : 0;
          recordAnswer(user?.uid ?? null, lessonId, section, index, !!correct, !!hintUsed)
            .catch(console.error);
          // Record XP + badge progress
          const streak = typeof event.detail?.streak === 'number' ? event.detail.streak : 0;
          gamOnAnswer(!!correct, mode as 'practice' | 'challenge', streak).catch(console.error);
          // Record per-question accuracy for admin dashboard
          if (user) {
            recordQuestionProgress(user, lessonId, section, index, !!correct)
              .catch(console.error);
          }
        }
      };

      engine.addEventListener('question', handleStateChange);
      engine.addEventListener('answered', handleAnswered);
      engine.addEventListener('answered', handleStateChange);
      engine.addEventListener('turn', handleStateChange);
      engine.addEventListener('tick', handleStateChange);
      engine.addEventListener('card', handleStateChange);
      engine.addEventListener('end', handleStateChange);

      engine.start();
      setLoading(false);
    } catch (err) {
      setError((err as Error).message || 'Failed to start game');
      setLoading(false);
    }
  }, [initialLesson, mode, selectedDuration]);

  // Fire onSessionEnd exactly once when the game transitions to over
  useEffect(() => {
    if (gameState && !gameState.running && !sessionEndedRef.current) {
      sessionEndedRef.current = true;
      onSessionEnd(mode as 'practice' | 'challenge' | 'teach').catch(console.error);
    }
  }, [gameState?.running]); // eslint-disable-line react-hooks/exhaustive-deps

  // ── CHALLENGE: Duration Picker ────────────────────────────────────────────
  if (mode === 'challenge' && selectedDuration === null) {
    return (
      <div className="fixed inset-0 flex flex-col overflow-y-auto" style={{ background: 'var(--ws-bg)' }}>
        <div className="max-w-md mx-auto w-full px-4 py-10 flex flex-col">
          {/* Back button */}
          <button
            onClick={() => router.push(`/class/${classNum}/${subject}/${lesson}`)}
            style={{
              background: 'none',
              border: 'none',
              color: 'var(--ws-text-muted)',
              fontWeight: 800,
              fontSize: '0.85rem',
              cursor: 'pointer',
              fontFamily: 'var(--font-nunito),sans-serif',
              marginBottom: '24px',
              textAlign: 'left',
            }}
          >
            ← Back
          </button>

          {/* Header */}
          <div className="text-center mb-8">
            <div className="text-5xl mb-3">⚡</div>
            <h2
              className="font-display text-3xl mb-1"
              style={{
                background: 'linear-gradient(135deg,#fbbf24,#f87171)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
              }}
            >
              Challenge Mode
            </h2>
            <p className="text-sm" style={{ color: 'var(--ws-text-muted)' }}>
              How long do you want to study?
            </p>
          </div>

          {/* Duration grid */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '12px',
              marginBottom: '32px',
            }}
          >
            {DURATION_OPTIONS.map((opt) => (
              <button
                key={opt.seconds}
                onClick={() => setSelectedDuration(opt.seconds)}
                style={{
                  background: 'var(--ws-card-inner)',
                  border: '2px solid rgba(251,191,36,0.25)',
                  borderRadius: '16px',
                  padding: '16px 8px',
                  cursor: 'pointer',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  gap: '4px',
                  transition: 'all 0.15s',
                }}
                onMouseEnter={(e) => {
                  (e.currentTarget as HTMLButtonElement).style.border = '2px solid #fbbf24';
                  (e.currentTarget as HTMLButtonElement).style.transform = 'translateY(-2px)';
                  (e.currentTarget as HTMLButtonElement).style.boxShadow = '0 6px 20px rgba(251,191,36,0.3)';
                }}
                onMouseLeave={(e) => {
                  (e.currentTarget as HTMLButtonElement).style.border = '2px solid rgba(251,191,36,0.25)';
                  (e.currentTarget as HTMLButtonElement).style.transform = 'none';
                  (e.currentTarget as HTMLButtonElement).style.boxShadow = 'none';
                }}
              >
                <span
                  className="font-display text-lg"
                  style={{ color: '#fbbf24' }}
                >
                  {opt.label}
                </span>
                <span
                  style={{
                    fontSize: '0.65rem',
                    color: 'var(--ws-text-muted)',
                    fontFamily: 'var(--font-nunito),sans-serif',
                    fontWeight: 700,
                  }}
                >
                  {opt.sublabel}
                </span>
              </button>
            ))}
          </div>

          {/* Info footer */}
          <div
            className="rounded-xl px-4 py-3 text-center text-xs"
            style={{
              background: 'rgba(251,191,36,0.08)',
              border: '1px solid rgba(251,191,36,0.2)',
              color: 'var(--ws-text-muted)',
              fontFamily: 'var(--font-nunito),sans-serif',
            }}
          >
            Questions keep cycling until time runs out. Your score keeps climbing!
          </div>
        </div>
      </div>
    );
  }

  // ── Loading ──────────────────────────────────────────────────────────────
  if (loading) {
    return (
      <div className="fixed inset-0 flex items-center justify-center" style={{ background: 'var(--ws-bg)' }}>
        <div className="text-center">
          <div className="text-6xl mb-4 animate-bounce">📚</div>
          <div className="font-display text-2xl" style={{ color: '#fbbf24' }}>Loading lesson…</div>
        </div>
      </div>
    );
  }

  // ── Error ────────────────────────────────────────────────────────────────
  if (error || !gameEngine || !gameState || !initialLesson) {
    return (
      <div className="fixed inset-0 flex items-center justify-center p-4" style={{ background: 'var(--ws-bg)' }}>
        <div className="text-center max-w-md">
          <div className="text-5xl mb-4">😬</div>
          <div className="font-display text-2xl text-theme mb-3">{error || 'Game failed to load'}</div>
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

  // ── Game Over ────────────────────────────────────────────────────────────
  if (!gameState.running) {
    return (
      <div className="fixed inset-0 overflow-y-auto" style={{ background: 'var(--ws-bg)' }}>
        {gameState.players.length > 1 ? (
          <div className="min-h-full py-8">
            <Podium
              players={gameState.players.map((p) => ({
                name: p.name,
                score: p.score,
                correct: p.correct,
                wrong: p.wrong,
                colorIdx: p.colorIdx,
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
              // Reset duration picker for challenge so they can change time
              if (mode === 'challenge') setSelectedDuration(null);
              else window.location.reload();
            }}
            onExit={() => router.push(`/class/${classNum}/${subject}/${lesson}`)}
          />
        )}
      </div>
    );
  }

  // ── TEACH MODE (Flashcard) ───────────────────────────────────────────────
  if (mode === 'teach') {
    const teachData = initialLesson.teach;

    if (!teachData || teachData.type !== 'flashcard') {
      return (
        <div className="fixed inset-0 flex items-center justify-center" style={{ background: 'var(--ws-bg)' }}>
          <div className="text-center">
            <div className="text-4xl mb-4">📭</div>
            <div className="font-display text-2xl text-theme mb-4">No teach content yet</div>
            <button
              onClick={() => router.back()}
              style={{ padding: '10px 24px', borderRadius: '14px', background: 'rgba(167,139,250,0.2)', border: '1px solid #a78bfa', color: '#a78bfa', fontWeight: 800, cursor: 'pointer' }}
            >
              ← Go Back
            </button>
          </div>
        </div>
      );
    }

    const totalCards = teachData.items?.length ?? 0;
    const cardIndex = gameState.currentCardIndex ?? 0;
    const item = teachData.items?.[cardIndex];
    const isFirst = cardIndex === 0;
    const isLast = cardIndex >= totalCards - 1;
    const progressPct = totalCards > 0 ? Math.round(((cardIndex + 1) / totalCards) * 100) : 0;

    return (
      <div className="fixed inset-0 flex flex-col overflow-hidden" style={{ background: 'var(--ws-bg)' }}>
        <ConfettiOverlay active={showConfetti} />

        {/* ── Top bar ── */}
        <div
          className="flex-shrink-0 flex items-center justify-between px-4 py-3"
          style={{ background: 'var(--ws-surface)', borderBottom: '1px solid var(--ws-border)' }}
        >
          <button
            onClick={() => router.push(`/class/${classNum}/${subject}/${lesson}`)}
            style={{ background: 'none', border: 'none', color: 'var(--ws-text-muted)', fontWeight: 800, fontSize: '0.85rem', cursor: 'pointer', fontFamily: 'var(--font-nunito),sans-serif' }}
          >
            ← Back
          </button>

          <div className="font-display text-base text-center" style={{
            background: 'linear-gradient(135deg,#fbbf24,#f87171)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
          }}>
            📚 {initialLesson.meta.title}
          </div>

          <div className="font-display text-sm" style={{ color: '#fbbf24' }}>
            {cardIndex + 1} / {totalCards}
          </div>
        </div>

        {/* ── Progress bar ── */}
        <div className="flex-shrink-0 h-1.5 mx-4 mt-1 rounded-full overflow-hidden" style={{ background: 'var(--ws-border)' }}>
          <div
            className="h-full rounded-full transition-all duration-500"
            style={{ width: `${progressPct}%`, background: 'linear-gradient(90deg,#a78bfa,#34d399)' }}
          />
        </div>

        {/* ── Flashcard area ── */}
        <div className="flex-1 flex items-center justify-center px-4 py-4 overflow-hidden">
          {item ? (
            <Flashcard
              front={item.front}
              back={item.back}
              hint={item.hint}
              index={cardIndex}
              total={totalCards}
              onSpeak={() => voiceManager?.speak(item.front)}
            />
          ) : (
            <div className="font-display text-xl text-theme opacity-40">No card data</div>
          )}
        </div>

        {/* ── Navigation ── */}
        <div
          className="flex-shrink-0 flex items-center justify-center gap-3 px-4 py-4"
          style={{ background: 'var(--ws-surface)', borderTop: '1px solid var(--ws-border)' }}
        >
          <button
            onClick={() => gameEngine.prevCard()}
            disabled={isFirst}
            style={{
              padding: '10px 24px',
              borderRadius: '30px',
              border: '2px solid rgba(167,139,250,0.35)',
              background: isFirst ? 'transparent' : 'rgba(167,139,250,0.12)',
              color: isFirst ? 'rgba(167,139,250,0.3)' : '#a78bfa',
              fontFamily: 'var(--font-nunito),sans-serif',
              fontWeight: 800,
              fontSize: '0.9rem',
              cursor: isFirst ? 'not-allowed' : 'pointer',
              transition: 'all 0.2s',
            }}
          >
            ← Previous
          </button>

          {isLast ? (
            <button
              onClick={() => gameEngine.endGame('manual')}
              style={{
                padding: '10px 28px',
                borderRadius: '30px',
                background: 'linear-gradient(135deg,#fbbf24,#f97316)',
                border: 'none',
                color: '#1a1a2e',
                fontFamily: 'var(--font-fredoka-one),cursive',
                fontSize: '1rem',
                fontWeight: 900,
                cursor: 'pointer',
                boxShadow: '0 4px 15px rgba(251,191,36,0.4)',
                transition: 'all 0.2s',
              }}
            >
              🏆 Finish!
            </button>
          ) : (
            <button
              onClick={() => gameEngine.nextCard()}
              style={{
                padding: '10px 28px',
                borderRadius: '30px',
                background: 'linear-gradient(135deg,#a78bfa,#f87171)',
                border: 'none',
                color: 'white',
                fontFamily: 'var(--font-fredoka-one),cursive',
                fontSize: '1rem',
                cursor: 'pointer',
                boxShadow: '0 4px 15px rgba(167,139,250,0.35)',
                transition: 'all 0.2s',
              }}
            >
              Next →
            </button>
          )}
        </div>
      </div>
    );
  }

  // ── PRACTICE / CHALLENGE MODE ────────────────────────────────────────────
  const q = gameState.currentQuestion as any;
  const displayText = q?.displayText || q?.question || q?.word || q?.statement || '';
  const spokenText  = q?.spokenText || displayText;
  const options     = q?.options ?? [];

  // Progress bar: time-based for challenge (since questionsCount is 999), question-based for practice
  const progressPct = mode === 'challenge' && gameState.totalTime > 0
    ? Math.min(100, Math.round(((gameState.totalTime - gameState.timeLeft) / gameState.totalTime) * 100))
    : Math.min(100, Math.round(((gameState.questionNumber || 0) / (gameState.totalQuestions || 20)) * 100));

  return (
    <div className="fixed inset-0 flex flex-col overflow-hidden" style={{ background: 'var(--ws-bg)' }}>
      <ConfettiOverlay active={showConfetti} />

      {/* ── Top bar: Score | Timer | Streak ── */}
      <div className="flex items-center justify-between flex-shrink-0" style={{ background: 'var(--ws-surface)', borderBottom: '1px solid var(--ws-border)' }}>
        <div className="text-center px-5 py-2 min-w-[80px]">
          <div className="text-xs uppercase tracking-widest mb-0.5" style={{ color: 'var(--ws-text-muted)' }}>Score</div>
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
            {initialLesson.meta.title}
          </div>
        )}

        <div className="text-center px-5 py-2 min-w-[80px]">
          <div className="text-xs uppercase tracking-widest mb-0.5" style={{ color: 'var(--ws-text-muted)' }}>Streak</div>
          <div className="font-display text-3xl" style={{ color: '#34d399' }}>
            {(currentPlayer?.streak || 0) > 0 ? `🔥${currentPlayer.streak}` : '0'}
          </div>
        </div>
      </div>

      {/* ── Progress bar ── */}
      <div className="flex-shrink-0 h-1.5 mx-4 my-1 rounded-full overflow-hidden" style={{ background: 'var(--ws-border)' }}>
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ width: `${progressPct}%`, background: 'linear-gradient(90deg,#a78bfa,#f87171)' }}
        />
      </div>

      {/* ── Question area ── */}
      <div className="flex-1 flex flex-col items-center justify-center gap-6 px-4 overflow-hidden">
        {gameState.currentQuestion && (
          <>
            <QuestionDisplay
              displayText={displayText}
              spokenText={spokenText}
              svgDiagram={q?.svg}
              onSpeak={() => voiceManager?.speak(spokenText)}
            />

            {options.length > 0 && (
              <OptionsGrid
                options={options}
                onSelect={(option) => gameEngine.checkAnswer(option)}
                columns={options.length <= 2 ? 1 : options.length <= 4 ? 2 : 3}
                disabled={gameState.lastAnswerValue !== undefined}
                correctOption={
                  gameState.lastAnswerCorrect
                    ? gameState.lastAnswerValue
                    : gameState.lastAnswerCorrect === false
                      ? gameState.correctAnswerValue
                      : undefined
                }
                wrongOption={gameState.lastAnswerCorrect === false ? gameState.lastAnswerValue : undefined}
              />
            )}
          </>
        )}
      </div>

      {/* ── End game button ── */}
      <div className="flex-shrink-0 flex justify-center py-3">
        <button
          onClick={() => gameEngine.endGame('manual')}
          style={{
            padding: '7px 18px',
            borderRadius: '10px',
            background: 'var(--ws-card2)',
            border: '1px solid var(--ws-border)',
            color: 'var(--ws-text-muted)',
            fontFamily: 'var(--font-nunito),sans-serif',
            fontWeight: 800,
            fontSize: '0.8rem',
            cursor: 'pointer',
          }}
        >
          ✕ End Game
        </button>
      </div>
    </div>
  );
}
