import {
  getAuth,
  GoogleAuthProvider,
  signInWithRedirect,
  getRedirectResult,
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

/**
 * Kick off Google sign-in using a full-page redirect.
 * This works reliably on any domain (GitHub Pages, custom domains, etc.)
 * without popup-blocker or cross-origin issues.
 * After Google authenticates the user, the page reloads and
 * `handleRedirectResult()` picks up the credential.
 */
export async function signInWithGoogle(): Promise<void> {
  await signInWithRedirect(_auth(), provider);
}

/**
 * Call this once on app startup (in AuthContext) to collect the credential
 * after Google redirects back. Returns the signed-in User or null if there
 * was no pending redirect.
 */
export async function handleRedirectResult(): Promise<User | null> {
  try {
    const result = await getRedirectResult(_auth());
    return result?.user ?? null;
  } catch (err) {
    console.error('Google redirect sign-in failed:', err);
    return null;
  }
}

export async function signOut(): Promise<void> {
  await fbSignOut(_auth());
}

export function onAuthChange(cb: (user: User | null) => void) {
  return onAuthStateChanged(_auth(), cb);
}
