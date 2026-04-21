import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  // Unique app identifier — matches what you'll register in Google Play & App Store
  appId: 'com.wonderstudy.app',
  appName: 'WonderStudy',

  // Points at the Next.js static export output folder.
  // Run `npm run build` before `npx cap sync` to refresh this.
  webDir: 'out',

  server: {
    // Allow the WebView to make requests to Firebase services.
    // androidScheme keeps URLs consistent between platforms.
    androidScheme: 'https',
  },

  android: {
    // Allow mixed content so Firebase Auth redirects work inside the WebView.
    allowMixedContent: true,
    // Tablet-first: allow all orientations (landscape is great for games).
    // Restrict to portrait-only on phones by adding a screen size qualifier in
    // AndroidManifest.xml later if needed.
    initialFocus: true,
  },

  ios: {
    // Use WKWebView (default modern WebView — required for App Store).
    contentInset: 'always',
    // Allow scrolling to be handled by the app, not the system.
    scrollEnabled: true,
  },

  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      launchAutoHide: true,
      backgroundColor: '#0d0d1a',
      androidSplashResourceName: 'splash',
      androidScaleType: 'CENTER_CROP',
      showSpinner: false,
    },
    StatusBar: {
      // Will be overridden at runtime based on the app's active theme.
      style: 'DARK',
      backgroundColor: '#0d0d1a',
    },
  },
};

export default config;
