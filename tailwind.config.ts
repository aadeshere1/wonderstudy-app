import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: "#0d0d1a",
        surface: "#161628",
        card: "#1e1e38",
        card2: "#252545",
        gold: "#fbbf24",
        coral: "#f87171",
        mint: "#34d399",
        purple: "#a78bfa",
        blue: "#60a5fa",
        pink: "#f472b6",
        muted: "rgba(240, 244, 255, 0.4)",
      },
      fontFamily: {
        display: ["var(--font-fredoka-one)"],
        body: ["var(--font-nunito)"],
      },
      keyframes: {
        twinkle: {
          "0%": { opacity: "0.05" },
          "100%": { opacity: "0.8" },
        },
        fadeUp: {
          "0%": { opacity: "0", transform: "translateY(16px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        shake: {
          "0%, 100%": { transform: "translateX(0)" },
          "25%": { transform: "translateX(-7px)" },
          "75%": { transform: "translateX(7px)" },
        },
        spin: {
          "0%": { transform: "rotate(0deg)" },
          "100%": { transform: "rotate(360deg)" },
        },
        speakPulse: {
          "0%, 100%": { boxShadow: "0 0 0 0 rgba(251, 191, 36, 0.4)" },
          "50%": { boxShadow: "0 0 0 10px rgba(251, 191, 36, 0)" },
        },
        cfFall: {
          "0%": { transform: "translateY(0) rotate(0)", opacity: "1" },
          "100%": { transform: "translateY(100vh) rotate(720deg)", opacity: "0" },
        },
      },
      animation: {
        twinkle: "twinkle var(--duration) ease-in-out infinite alternate",
        fadeUp: "fadeUp 0.4s ease",
        shake: "shake 0.35s ease",
        spin: "spin 0.7s linear infinite",
        speakPulse: "speakPulse 1s ease infinite",
        cfFall: "cfFall 1.2s ease-in forwards",
      },
      boxShadow: {
        glow: "0 4px 15px rgba(167, 139, 250, 0.35)",
        correct: "0 4px 12px rgba(52, 211, 153, 0.4)",
      },
    },
  },
  plugins: [],
};

export default config;
