'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { getTotalDueCount } from '@/lib/srs/store';

export default function SRSDueWidget() {
  const { user, loading } = useAuth();
  const [totalDue, setTotalDue] = useState<number | null>(null);

  useEffect(() => {
    if (loading) return;
    getTotalDueCount(user?.uid ?? null).then(setTotalDue);
  }, [user, loading]);

  // Hide while auth is loading or if nothing is due
  if (loading || totalDue === null || totalDue === 0) return null;

  return (
    <div
      className="rounded-2xl px-5 py-4 flex items-center gap-4 mb-5"
      style={{
        background: 'linear-gradient(135deg, rgba(99,102,241,0.18), rgba(167,139,250,0.12))',
        border: '1px solid rgba(99,102,241,0.35)',
      }}
    >
      <div className="text-3xl flex-shrink-0">🔁</div>
      <div className="flex-1 min-w-0">
        <div className="font-display text-base text-white leading-tight">
          {totalDue} card{totalDue !== 1 ? 's' : ''} due for review
        </div>
        <div className="text-xs mt-0.5" style={{ color: 'rgba(240,244,255,0.45)' }}>
          Keep your streak alive with spaced repetition
        </div>
      </div>
      <div
        className="flex-shrink-0 text-xs font-bold px-3 py-1.5 rounded-xl"
        style={{
          background: 'linear-gradient(135deg,#6366f1,#a78bfa)',
          color: 'white',
          whiteSpace: 'nowrap',
        }}
      >
        Go review →
      </div>
    </div>
  );
}
