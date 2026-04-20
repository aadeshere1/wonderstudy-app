'use client';

import { useState } from 'react';
import { Chip } from '@/components/ui';

export interface PlayerSetupProps {
  players: Array<{ name: string; colorIdx: number }>;
  onPlayersChange: (players: Array<{ name: string; colorIdx: number }>) => void;
  maxPlayers?: number;
}

const colorOptions = [
  { idx: 0, name: 'Blue', emoji: '🟦' },
  { idx: 1, name: 'Coral', emoji: '🟥' },
  { idx: 2, name: 'Mint', emoji: '🟩' },
  { idx: 3, name: 'Gold', emoji: '🟨' },
  { idx: 4, name: 'Purple', emoji: '🟪' },
  { idx: 5, name: 'Pink', emoji: '💗' },
];

export const PlayerSetup = ({
  players,
  onPlayersChange,
  maxPlayers = 4,
}: PlayerSetupProps) => {
  const [newPlayerName, setNewPlayerName] = useState('');
  const [editingIdx, setEditingIdx] = useState<number | null>(null);

  const handleAddPlayer = () => {
    if (newPlayerName.trim() && players.length < maxPlayers) {
      onPlayersChange([
        ...players,
        { name: newPlayerName, colorIdx: players.length % 6 },
      ]);
      setNewPlayerName('');
    }
  };

  const handleRemovePlayer = (idx: number) => {
    onPlayersChange(players.filter((_, i) => i !== idx));
  };

  const handleUpdateName = (idx: number, name: string) => {
    const updated = [...players];
    updated[idx].name = name;
    onPlayersChange(updated);
  };

  const handleColorChange = (idx: number, colorIdx: number) => {
    const updated = [...players];
    updated[idx].colorIdx = colorIdx;
    onPlayersChange(updated);
  };

  return (
    <div className="space-y-4">
      <h3 className="text-sm font-black text-theme uppercase tracking-wider">
        👥 Players ({players.length}/{maxPlayers})
      </h3>

      {/* Player List */}
      <div className="space-y-2">
        {players.map((player, idx) => (
          <div
            key={idx}
            className="bg-card border border-white/10 rounded-lg p-3 space-y-2"
          >
            {/* Name Input */}
            <div className="flex gap-2 items-center">
              <input
                type="text"
                value={editingIdx === idx ? player.name : player.name}
                onChange={(e) =>
                  editingIdx === idx && handleUpdateName(idx, e.target.value)
                }
                onFocus={() => setEditingIdx(idx)}
                onBlur={() => setEditingIdx(null)}
                className="flex-1 px-3 py-2 rounded-lg bg-card2 border border-white/10 text-theme focus:outline-none focus:ring-2 focus:ring-purple/50"
              />
              <div className="text-lg">
                {colorOptions.find((c) => c.idx === player.colorIdx)?.emoji}
              </div>
              {players.length > 1 && (
                <button
                  onClick={() => handleRemovePlayer(idx)}
                  className="px-2 py-2 rounded-lg bg-coral/20 hover:bg-coral/30 text-coral font-black transition-all"
                >
                  ✕
                </button>
              )}
            </div>

            {/* Color Picker */}
            <div className="flex gap-1 flex-wrap">
              {colorOptions.map((color) => (
                <button
                  key={color.idx}
                  onClick={() => handleColorChange(idx, color.idx)}
                  className={`p-2 rounded transition-all ${
                    player.colorIdx === color.idx
                      ? 'ring-2 ring-white scale-110'
                      : 'opacity-60 hover:opacity-100'
                  }`}
                  title={color.name}
                >
                  {color.emoji}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Add Player Form */}
      {players.length < maxPlayers && (
        <div className="flex gap-2">
          <input
            type="text"
            value={newPlayerName}
            onChange={(e) => setNewPlayerName(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAddPlayer()}
            placeholder="Player name..."
            maxLength={20}
            className="flex-1 px-3 py-2 rounded-lg bg-card border border-white/10 text-theme placeholder-muted focus:outline-none focus:ring-2 focus:ring-purple/50"
          />
          <button
            onClick={handleAddPlayer}
            disabled={!newPlayerName.trim()}
            className="px-4 py-2 rounded-lg bg-purple hover:bg-purple/80 text-theme font-black transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            +
          </button>
        </div>
      )}

      {/* Info */}
      {players.length === 0 && (
        <div className="text-sm text-muted bg-blue/10 px-3 py-2 rounded-lg">
          💡 Add at least 1 player to start
        </div>
      )}
    </div>
  );
};
