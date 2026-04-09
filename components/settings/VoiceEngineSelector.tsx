'use client';

import { ToggleSwitch } from '@/components/ui';

export interface VoiceEngineSelectorProps {
  currentEngine: 'browser' | 'elevenlabs';
  onEngineChange: (engine: 'browser' | 'elevenlabs') => void;
  speed: 'slow' | 'normal' | 'fast';
  onSpeedChange: (speed: 'slow' | 'normal' | 'fast') => void;
  isAvailable?: {
    browser: boolean;
    elevenlabs: boolean;
  };
}

export const VoiceEngineSelector = ({
  currentEngine,
  onEngineChange,
  speed,
  onSpeedChange,
  isAvailable = { browser: true, elevenlabs: true },
}: VoiceEngineSelectorProps) => {
  return (
    <div className="space-y-4">
      <div>
        <h3 className="text-sm font-black text-white uppercase tracking-wider mb-3">
          🔊 Voice Engine
        </h3>
        <div className="space-y-2">
          {/* Browser Voice */}
          <button
            onClick={() => isAvailable.browser && onEngineChange('browser')}
            disabled={!isAvailable.browser}
            className={`w-full text-left px-4 py-3 rounded-lg border transition-all ${
              currentEngine === 'browser'
                ? 'bg-blue/20 border-blue'
                : 'bg-card border-white/10 hover:border-white/20'
            } ${!isAvailable.browser ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
          >
            <div className="font-black text-white">Browser Voice</div>
            <div className="text-xs text-muted mt-1">
              {isAvailable.browser ? 'Built-in system voices' : 'Not available'}
            </div>
          </button>

          {/* ElevenLabs Voice */}
          <button
            onClick={() => isAvailable.elevenlabs && onEngineChange('elevenlabs')}
            disabled={!isAvailable.elevenlabs}
            className={`w-full text-left px-4 py-3 rounded-lg border transition-all ${
              currentEngine === 'elevenlabs'
                ? 'bg-purple/20 border-purple'
                : 'bg-card border-white/10 hover:border-white/20'
            } ${!isAvailable.elevenlabs ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
          >
            <div className="font-black text-white">ElevenLabs</div>
            <div className="text-xs text-muted mt-1">
              {isAvailable.elevenlabs ? 'Premium natural voices' : 'Not available'}
            </div>
          </button>
        </div>
      </div>

      {/* Speed Control */}
      <div>
        <h3 className="text-sm font-black text-white uppercase tracking-wider mb-3">
          ⚡ Speed
        </h3>
        <div className="grid grid-cols-3 gap-2">
          {(['slow', 'normal', 'fast'] as const).map((s) => (
            <button
              key={s}
              onClick={() => onSpeedChange(s)}
              className={`px-3 py-2 rounded-lg font-black text-sm transition-all ${
                speed === s
                  ? 'bg-gold/20 text-gold border border-gold'
                  : 'bg-card border border-white/10 text-white hover:border-white/20'
              }`}
            >
              {s === 'slow' ? '🐢' : s === 'normal' ? '🐇' : '⚡'}
              <div className="text-xs mt-1 capitalize">{s}</div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
