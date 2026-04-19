import { getAuth, GoogleAuthProvider, signInWithPopup, signOut as fbSignOut, onAuthStateChanged, User } from 'firebase/auth';
import app from './config';

export const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export async function signInWithGoogle(): Promise<User | null> {
  try {
    const result = await signInWithPopup(auth, provider);
    return result.user;
  } catch (err) {
    console.error('Google sign-in failed:', err);
    return null;
  }
}

export async function signOut(): Promise<void> {
  await fbSignOut(auth);
}

export function onAuthChange(cb: (user: User | null) => void) {
  return onAuthStateChanged(auth, cb);
}
