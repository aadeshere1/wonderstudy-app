/**
 * Firestore singleton with offline persistence enabled.
 *
 * Import `fdb` from here (not directly from 'firebase/firestore') anywhere
 * you need a Firestore instance. This ensures persistence is initialised
 * exactly once, regardless of how many modules import it.
 *
 * Offline behaviour:
 *  - All reads are served from the local IndexedDB cache when offline.
 *  - All writes are queued locally and automatically replayed when the
 *    device reconnects — zero extra code required at the call site.
 *  - Auth tokens are cached by Firebase Auth SDK separately, so signed-in
 *    students remain authenticated indefinitely without a network round-trip.
 */

import {
  getFirestore,
  initializeFirestore,
  persistentLocalCache,
  persistentMultipleTabManager,
} from 'firebase/firestore';
import app from '@/lib/firebase/config';

// Initialise exactly once. The try/catch handles hot-reload double-init:
// initializeFirestore throws if Firestore was already initialised for this
// app instance, so we fall back to getFirestore() which returns the existing one.
function createFirestore() {
  try {
    // persistentLocalCache = IndexedDB-backed offline cache.
    // persistentMultipleTabManager = safe to use across multiple browser tabs
    // (important for web; harmless on mobile where only one tab exists).
    return initializeFirestore(app, {
      localCache: persistentLocalCache({
        tabManager: persistentMultipleTabManager(),
      }),
    });
  } catch {
    // initializeFirestore throws if Firestore was already initialised for this
    // app instance (e.g. on hot reload). Fall back to the existing instance.
    return getFirestore(app);
  }
}

const fdb = createFirestore();

export default fdb;
