'use client';

import { useState } from 'react';
import { ToggleSwitch, Button } from '@/components/ui';
import { VoiceEngineSelector } from './VoiceEngineSelector';
import { PlayerSetup } from './PlayerSetup';

export interface SettingsPanelProps {
  onClose?: () => void;
  showCloseButton?: boolean;
  compact?: boolean;
}

interface Settings {
  players: Array<{ name: string; colorIdx: number }>;
  voiceEngine: 'browser' | 'elevenlabs';
  voiceSpeed: 'slow' | 'normal' | 'fast';
  speakQuestions: boolean;
  speakCorrect: boolean;
  speakWrong: boolean;
  soundEffects: boolean;
}

export const SettingsPanel = ({
  onClose,
  showCloseButton = true,
  compact = false,
}: SettingsPanelProps) => {
  const [settings, setSettings] = useState<Settings>(() => {
    if (typeof window === 'undefined') {
      return {
        players: [{ name: 'Player 1', colorIdx: 0 }],
        voiceEngine: 'browser',
        voiceSpeed: 'normal',
        speakQuestions: true,
        speakCorrect: true,
        speakWrong: true,
        soundEffects: true,
      };
    }

    const saved = localStorage.getItem('wsSettings');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch {
        // Fall through to defaults
      }
    }

    return {
      players: [{ name: 'Player 1', colorIdx: 0 }],
      voiceEngine: 'browser',
      voiceSpeed: 'normal',
      speakQuestions: true,
      speakCorrect: true,
      speakWrong: true,
      soundEffects: true,
    };
  });

  const saveSettings = (updated: Partial<Settings>) => {
    const newSettings = { ...settings, ...updated };
    setSettings(newSettings);
    if (typeof window !== 'undefined') {
      localStorage.setItem('wsSettings', JSON.stringify(newSettings));
    }
  };

  const containerClass = compact
    ? 'space-y-4 text-sm'
    : 'space-y-6 max-w-xl';

  return (
    <div className={containerClass}>
      {/* Header */}
      {!compact && (
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-black text-white">⚙️ Settings</h2>
          {showCloseButton && onClose && (
            <button
              onClick={onClose}
              className="px-3 py-2 rounded-lg bg-card2 hover:bg-card border border-white/10 text-white transition-all"
            >
              ✕
            </button>
          )}
        </div>
      )}

      {/* Voice Settings */}
      <div className="bg-card border border-white/10 rounded-lg p-4 space-y-4">
        <VoiceEngineSelector
          currentEngine={settings.voiceEngine}
          onEngineChange={(engine) => saveSettings({ voiceEngine: engine })}
          speed={settings.voiceSpeed}
          onSpeedChange={(speed) => saveSettings({ voiceSpeed: speed })}
        />
      </div>

      {/* Audio Toggles */}
      <div className="bg-card border border-white/10 rounded-lg p-4 space-y-3">
        <h3 className="text-sm font-black text-white uppercase tracking-wider">
          🎵 Audio
        </h3>

        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-white font-semibold">Speak Questions</label>
            <ToggleSwitch
              checked={settings.speakQuestions}
              onChange={(val) => saveSettings({ speakQuestions: val })}
            />
          </div>

          <div className="flex items-center justify-between">
            <label className="text-white font-semibold">Speak Correct</label>
            <ToggleSwitch
              checked={settings.speakCorrect}
              onChange={(val) => saveSettings({ speakCorrect: val })}
            />
          </div>

          <div className="flex items-center justify-between">
            <label className="text-white font-semibold">Speak Wrong</label>
            <ToggleSwitch
              checked={settings.speakWrong}
              onChange={(val) => saveSettings({ speakWrong: val })}
            />
          </div>

          <div className="flex items-center justify-between">
            <label className="text-white font-semibold">Sound Effects</label>
            <ToggleSwitch
              checked={settings.soundEffects}
              onChange={(val) => saveSettings({ soundEffects: val })}
            />
          </div>
        </div>
      </div>

      {/* Player Setup */}
      <div className="bg-card border border-white/10 rounded-lg p-4">
        <PlayerSetup
          players={settings.players}
          onPlayersChange={(players) => saveSettings({ players })}
        />
      </div>

      {/* Action Buttons */}
      {!compact && (
        <div className="flex gap-2">
          {onClose && (
            <Button variant="primary" size="md" onClick={onClose} className="flex-1">
              ← Back
            </Button>
          )}
        </div>
      )}
    </div>
  );
};
