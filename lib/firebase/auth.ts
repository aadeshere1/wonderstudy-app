import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signOut as fbSignOut,
  onAuthStateChanged,
  type User,
} from 'firebase/auth';
import app from './config';

// Lazy accessor — avoids calling getAuth() at module evaluation time,
// which would throw auth/invalid-api-key during SSR/prerender when
// NEXT_PUBLIC_FIREBASE_* env vars are absent from the build environment.
function _auth() {
  return getAuth(app);
}

const provider = new GoogleAuthProvider();

export async function signInWithGoogle(): Promise<User | null> {
  try {
    const result = await signInWithPopup(_auth(), provider);
    return result.user;
  } catch (err) {
    console.error('Google sign-in failed:', err);
    return null;
  }
}

export async function signOut(): Promise<void> {
  await fbSignOut(_auth());
}

export function onAuthChange(cb: (user: User | null) => void) {
  return onAuthStateChanged(_auth(), cb);
}
