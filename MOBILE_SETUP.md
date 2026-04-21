# Sikshya Mobile App — Setup Guide

The mobile app uses **Capacitor 8** to wrap the Next.js static export into a native Android and iOS app. The web app source is unchanged; Capacitor just packages the `out/` build output as a native app.

---

## Prerequisites

### Both platforms
- Node.js 18+ and npm (already used for the web app)

### Android
- [Android Studio](https://developer.android.com/studio) (latest stable)
- Android SDK: API 28+ (Android 9.0) — install via Android Studio SDK Manager
- JDK 17 (bundled with Android Studio)
- A physical Android tablet **or** an Android Virtual Device (AVD) configured as a tablet (e.g. Pixel Tablet API 34)

### iOS
- macOS only (Xcode is Mac-exclusive)
- [Xcode 15+](https://developer.apple.com/xcode/) from the Mac App Store
- CocoaPods: `sudo gem install cocoapods`
- An Apple Developer account (free for simulator testing; $99/yr for device + App Store)

---

## First-time setup

```bash
# 1. Build the Next.js static export and sync it into the native projects
npm run build:mobile

# This runs:
#   npm run build        → generates the out/ folder
#   npx cap sync         → copies out/ into android/app/src/main/assets/public
#                          and ios/App/App/public
```

After `build:mobile` finishes you'll see:
```
✔ Copying web assets from out to android/app/src/main/assets/public
✔ Copying web assets from out to ios/App/App/public
✔ copy android
✔ copy ios
✔ update android
✔ update ios
```

---

## Running on Android

```bash
# Open the Android project in Android Studio
npm run cap:android
```

Inside Android Studio:
1. Wait for Gradle sync to finish (first run can take a few minutes)
2. Select your target device (tablet AVD or connected physical device)
3. Click **Run ▶**

The app will be installed and launched. Every time you change the web code, run `npm run build:mobile` then hit Run again in Android Studio — no Gradle rebuild needed, only the web assets are updated.

### Tablet emulator setup (Android Studio)
1. Tools → Device Manager → Create Virtual Device
2. Choose **Tablet** category → Pixel Tablet
3. System Image: API 34 (Android 14) — download if needed
4. Finish → Launch the AVD

---

## Running on iOS

```bash
# Open the Xcode project
npm run cap:ios
```

Inside Xcode:
1. Select the `App` scheme and your target (simulator or physical device)
2. For a physical device you'll need to set a **Team** in Signing & Capabilities
3. Click **Run ▶**

### CocoaPods (first run only)
```bash
cd ios/App
pod install
cd ../..
```

### iPad simulator setup (Xcode)
Window → Devices and Simulators → + → iPad Pro (12.9-inch) (6th generation)

---

## Day-to-day workflow

| What changed | Command to run |
|---|---|
| Web app code | `npm run build:mobile` then Run in IDE |
| Native plugins added | `npm run build:mobile` (includes `cap sync`) |
| Only testing on web | `npm run dev` as normal |

---

## Updating web assets only (faster)

If you just changed JS/CSS and don't need a full Gradle/Xcode rebuild:

```bash
npm run build          # regenerate out/
npx cap copy android   # copy assets only, skip plugin sync
npx cap copy ios
```

Then in Android Studio: Run ▶ (it detects asset changes and re-deploys without rebuilding).

---

## Environment variables on mobile

The `.env.local` Firebase keys are baked into the static export at build time via `NEXT_PUBLIC_*` variables. They work the same on mobile as on web — just make sure `.env.local` is present before running `npm run build:mobile`.

---

## App identifiers

| Field | Value |
|---|---|
| App ID | `com.sikshya.app` |
| Android package | `com.sikshya.app` |
| iOS bundle ID | `com.sikshya.app` |
| Display name | Sikshya |

---

## Google Sign-In on mobile

Google Sign-In via popup/redirect does not work reliably in a native WebView. This is a known issue that will be addressed in **Phase 4** by adding the `@codetrix-studio/capacitor-google-auth` plugin, which uses the native Google Sign-In SDK.

For now, sign-in works on the web app as normal. Students who were already signed in (cached auth token) will stay signed in on mobile indefinitely.

---

## Project structure

```
sikshya-app/
├── android/              ← Android Studio project (git-tracked)
│   └── app/
│       └── src/main/
│           ├── assets/public/   ← auto-populated by cap sync (gitignored)
│           └── java/com/sikshya/app/MainActivity.java
├── ios/                  ← Xcode project (git-tracked)
│   └── App/
│       └── App/public/  ← auto-populated by cap sync (gitignored)
├── out/                  ← Next.js static export (gitignored)
├── capacitor.config.ts   ← Capacitor configuration
└── package.json          ← includes build:mobile, cap:android, cap:ios scripts
```

---

## Next phases

- **Phase 2** — Tablet-specific UI layer (CSS, touch targets, safe areas)
- **Phase 3** — Native enhancements (haptics, push notifications, offline indicator, keep-awake)
- **Phase 4** — Native Google Sign-In
- **Phase 5** — Build pipeline (signed APK/AAB, App Store IPA)
- **Phase 6** — Google Play and App Store submission
