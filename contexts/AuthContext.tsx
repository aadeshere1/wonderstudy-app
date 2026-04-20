'use client';

import { createContext, useContext, useEffect, useRef, useState, ReactNode } from 'react';
import { User } from 'firebase/auth';
import { signInWithGoogle, handleRedirectResult, signOut, onAuthChange } from '@/lib/firebase/auth';
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
    let unsub: (() => void) | null = null;

    const initialize = async () => {
      // IMPORTANT: await getRedirectResult() BEFORE setting up onAuthStateChanged.
      //
      // When the user is redirected back from Google, the auth token is not yet
      // in localStorage — it only lands there after getRedirectResult() calls
      // signInWithCredential internally. If we set up the listener first,
      // onAuthStateChanged fires with null, sets loading=false, and shows
      // "Sign In" — even though the user just authenticated. Awaiting
      // getRedirectResult() first means onAuthStateChanged sees the correct
      // signed-in state on its very first emission.
      await handleRedirectResult();

      unsub = onAuthChange(async (u) => {
        if (u && syncedUidRef.current !== u.uid) {
          // Merge any local guest SRS/gam progress to Firestore
          mergeLocalToFirestore(u.uid).catch(console.error);
        }
        if (!u) syncedUidRef.current = null; // reset on sign-out
        setUser(u);
        setLoading(false);
      });
    };

    initialize().catch((err) => {
      console.error('[auth] initialization failed:', err);
      setLoading(false); // fail open — don't leave app stuck in loading state
    });

    return () => { unsub?.(); };
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
    const u = await signInWithGoogle();
    // signInWithPopup returns the user directly; signInWithRedirect returns
    // null and navigates away (result picked up by handleRedirectResult on return).
    if (u) setUser(u);
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
