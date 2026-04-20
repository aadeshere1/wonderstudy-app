import { initializeApp, getApps } from 'firebase/app';

// Use empty-string fallbacks so initializeApp never receives `undefined`.
// The actual values must be present at runtime (client-side); build-time
// prerendering only evaluates the module — it never calls Firebase services,
// so empty strings here are safe during SSR/static export.
const firebaseConfig = {
  apiKey:            process.env.NEXT_PUBLIC_FIREBASE_API_KEY            ?? '',
  authDomain:        process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN        ?? '',
  projectId:         process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID         ?? '',
  storageBucket:     process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET     ?? '',
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID ?? '',
  appId:             process.env.NEXT_PUBLIC_FIREBASE_APP_ID             ?? '',
};

// Prevent re-initialising on hot reload
const app = getApps().length ? getApps()[0] : initializeApp(firebaseConfig);

export default app;
