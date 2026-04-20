'use client';

export interface PlayerResult {
  name: string;
  score: number;
  correct: number;
  wrong: number;
  colorIdx: number;
}

export interface PodiumProps {
  players: PlayerResult[];
  showMedals?: boolean;
}

const colorMap: Record<number, string> = {
  0: 'bg-blue/20 border-blue text-blue',
  1: 'bg-coral/20 border-coral text-coral',
  2: 'bg-mint/20 border-mint text-mint',
  3: 'bg-gold/20 border-gold text-gold',
  4: 'bg-purple/20 border-purple text-purple',
  5: 'bg-pink/20 border-pink text-pink',
};

const medalEmojis = ['🥇', '🥈', '🥉'];

export const Podium = ({ players, showMedals = true }: PodiumProps) => {
  // Sort by score descending
  const sorted = [...players].sort((a, b) => b.score - a.score);
  const topThree = sorted.slice(0, 3);

  // Arrange for podium display (2nd place on left, 1st in center, 3rd on right)
  const podiumOrder = [topThree[1], topThree[0], topThree[2]].filter(Boolean);
  const heights = [70, 100, 50]; // percentages for visual podium effect

  return (
    <div className="flex flex-col items-center gap-8 w-full">
      {/* Podium Visual */}
      <div className="flex items-flex-end justify-center gap-4 h-48 px-4">
        {podiumOrder.map((player, idx) => {
          if (!player) return null;

          const positionIndex = topThree.indexOf(player);
          const colorClass = colorMap[player.colorIdx];
          const height = heights[idx];
          const medal = showMedals ? medalEmojis[positionIndex] : null;

          return (
            <div key={player.name} className="flex flex-col items-center gap-2">
              {/* Name */}
              <div className="text-sm font-black text-center text-theme max-w-20 truncate">
                {player.name}
              </div>

              {/* Podium Box */}
              <div
                className={`${colorClass} border-2 rounded-lg p-3 text-center w-24 transition-transform`}
                style={{ height: `${height}px` }}
              >
                <div className="text-xs text-muted uppercase tracking-wider mb-1">
                  Position {positionIndex + 1}
                </div>
                <div className="text-2xl font-black text-theme">{player.score}</div>
                <div className="text-xs text-muted mt-1">points</div>
              </div>

              {/* Medal */}
              {medal && <div className="text-3xl">{medal}</div>}
            </div>
          );
        })}
      </div>

      {/* Full Leaderboard */}
      <div className="w-full max-w-md">
        <h3 className="text-lg font-black text-theme mb-3">Final Results</h3>
        <div className="space-y-2">
          {sorted.map((player, idx) => {
            const colorClass = colorMap[player.colorIdx];
            const total = player.correct + player.wrong;
            const accuracy = total > 0 ? Math.round((player.correct / total) * 100) : 0;

            return (
              <div
                key={player.name}
                className={`${colorClass} border rounded-lg p-3 flex items-center justify-between`}
              >
                <div className="flex items-center gap-3 flex-1">
                  <div className="font-black text-lg w-8">#{idx + 1}</div>
                  <div>
                    <div className="font-black text-theme text-sm">{player.name}</div>
                    <div className="text-xs text-muted">
                      {player.correct}✓ {player.wrong}✗ {accuracy}%
                    </div>
                  </div>
                </div>
                <div className="font-black text-lg">{player.score}</div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
