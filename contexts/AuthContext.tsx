'use client';

import { createContext, useContext, useEffect, useRef, useState, ReactNode } from 'react';
import { User } from 'firebase/auth';
import { signInWithGoogle, signOut, onAuthChange } from '@/lib/firebase/auth';
import { mergeLocalToFirestore } from '@/lib/srs/store';

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  signIn: () => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue>({
  user: null,
  loading: true,
  signIn: async () => {},
  signOut: async () => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser]       = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  // Track which UID we've already written a profile for this session
  const syncedUidRef = useRef<string | null>(null);

  // Auth state listener — keep lean, no Firestore writes here
  useEffect(() => {
    const unsub = onAuthChange(async (u) => {
      if (u && syncedUidRef.current !== u.uid) {
        // Merge any local guest SRS/gam progress to Firestore
        mergeLocalToFirestore(u.uid).catch(console.error);
      }
      if (!u) syncedUidRef.current = null; // reset on sign-out
      setUser(u);
      setLoading(false);
    });
    return unsub;
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Write profile to publicProgress once per sign-in session.
  // Runs AFTER React commits user state, and calls getIdToken() to guarantee
  // the auth token is flushed to the Firestore SDK before the write.
  useEffect(() => {
    if (!user || syncedUidRef.current === user.uid) return;
    syncedUidRef.current = user.uid;

    const writeProfile = async () => {
      try {
        // Ensure the ID token is available to Firestore before writing
        await user.getIdToken();
        const { getFirestore, doc, setDoc } = await import('firebase/firestore');
        const { default: app } = await import('@/lib/firebase/config');
        const db  = getFirestore(app);
        const ref = doc(db, 'publicProgress', user.uid);
        const now = new Date().toISOString();
        await setDoc(ref, {
          uid:      user.uid,
          name:     user.displayName ?? 'Student',
          email:    user.email ?? '',
          photoURL: user.photoURL ?? '',
          lastSeen: now,
          joinedAt: now, // merge: true won't overwrite joinedAt on subsequent logins
        }, { merge: true });
      } catch (e) {
        console.error('publicProgress profile write failed', e);
        syncedUidRef.current = null; // allow retry on next render
      }
    };
    writeProfile();
  }, [user]);

  const handleSignIn = async () => {
    await signInWithGoogle();
  };

  const handleSignOut = async () => {
    await signOut();
  };

  return (
    <AuthContext.Provider value={{ user, loading, signIn: handleSignIn, signOut: handleSignOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
