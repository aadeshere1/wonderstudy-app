import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
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
 * Sign in with Google.
 *
 * Strategy:
 *  1. Try signInWithPopup — best UX, works on desktop once the domain is
 *     listed in Firebase → Authentication → Authorized domains.
 *  2. If the browser blocks the popup (mobile, strict settings), fall back
 *     to signInWithRedirect, which navigates the whole page to Google and
 *     back. AuthContext's handleRedirectResult() picks up the result on return.
 */
export async function signInWithGoogle(): Promise<User | null> {
  try {
    const result = await signInWithPopup(_auth(), provider);
    return result.user;
  } catch (err: any) {
    const code = err?.code ?? '';
    if (code === 'auth/popup-blocked' || code === 'auth/popup-closed-by-user') {
      // Popup was suppressed — fall back to full-page redirect
      await signInWithRedirect(_auth(), provider);
      return null; // page navigates away; result handled on return via handleRedirectResult
    }
    console.error('[auth] signInWithGoogle failed:', err);
    return null;
  }
}

/**
 * Called once on app startup (in AuthContext) to collect a credential
 * after Google redirects the user back from a signInWithRedirect flow.
 * Returns the User if a redirect was pending, null on normal loads.
 */
export async function handleRedirectResult(): Promise<User | null> {
  try {
    const result = await getRedirectResult(_auth());
    return result?.user ?? null;
  } catch (err) {
    // auth/unauthorized-domain or network errors — log but don't crash
    console.error('[auth] getRedirectResult failed:', err);
    return null;
  }
}

export async function signOut(): Promise<void> {
  await fbSignOut(_auth());
}

export function onAuthChange(cb: (user: User | null) => void) {
  return onAuthStateChanged(_auth(), cb);
}
