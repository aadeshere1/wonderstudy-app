import { Settings } from "@/lib/engine/types";

const NUM_WORDS = [
  "zero",
  "one",
  "two",
  "three",
  "four",
  "five",
  "six",
  "seven",
  "eight",
  "nine",
  "ten",
  "eleven",
  "twelve",
];

const CHEERS = [
  "Amazing!",
  "Brilliant!",
  "Fantastic!",
  "Spot on!",
  "Perfect!",
  "Super!",
  "Excellent!",
  "Great job!",
  "Wonderful!",
];

// Voice preference ranking
const PREFERRED_VOICE_HINTS = [
  "Google UK English Female",
  "Google UK English Male",
  "Microsoft Aria",
  "Microsoft Jenny",
  "Microsoft Guy",
  "Microsoft Zira",
  "Microsoft David",
  "Samantha",
  "Karen",
  "Moira",
  "Fiona",
  "Daniel",
  "Google US English",
];

const SPEECH_RATES = {
  slow: 0.8,
  normal: 0.92,
  fast: 1.25,
};

export class VoiceManager {
  private settings: Settings;
  private currentUtterance: SpeechSynthesisUtterance | null = null;
  private browserVoices: SpeechSynthesisVoice[] = [];

  constructor(settings: Settings) {
    this.settings = settings;
    this.loadBrowserVoices();
  }

  /**
   * Load available browser voices
   */
  async loadBrowserVoices(): Promise<void> {
    return new Promise((resolve) => {
      if (!("speechSynthesis" in window)) {
        console.warn("Speech Synthesis not supported");
        resolve();
        return;
      }

      // Voices may not be loaded immediately
      const synth = window.speechSynthesis;

      const loadVoices = () => {
        const voices = synth.getVoices();
        this.browserVoices = voices.filter(
          (voice) =>
            voice.lang &&
            (voice.lang.startsWith("en") ||
              voice.lang.toLowerCase().startsWith("en"))
        );
        resolve();
      };

      if (synth.getVoices().length > 0) {
        loadVoices();
      } else {
        synth.onvoiceschanged = loadVoices;
      }
    });
  }

  /**
   * Get the best matching browser voice based on preferences
   */
  private getBestBrowserVoice(): SpeechSynthesisVoice | undefined {
    // If user has selected a specific voice, use it
    if (this.settings.selectedVoiceURI) {
      const found = this.browserVoices.find(
        (v) => v.voiceURI === this.settings.selectedVoiceURI
      );
      if (found) return found;
    }

    // Try to find preferred voices in order
    for (const hint of PREFERRED_VOICE_HINTS) {
      const voice = this.browserVoices.find((v) =>
        v.name.includes(hint)
      );
      if (voice) return voice;
    }

    // Fallback to first English voice
    return this.browserVoices[0];
  }

  /**
   * Get all available browser voices
   */
  getAvailableVoices(): SpeechSynthesisVoice[] {
    return this.browserVoices;
  }

  /**
   * Speak using browser speech synthesis
   */
  async speakBrowser(text: string, rate: string): Promise<void> {
    return new Promise((resolve) => {
      if (!("speechSynthesis" in window)) {
        console.warn("Speech Synthesis not supported");
        resolve();
        return;
      }

      // Cancel any ongoing speech
      window.speechSynthesis.cancel();

      const synth = window.speechSynthesis;
      const utterance = new SpeechSynthesisUtterance(text);

      const voice = this.getBestBrowserVoice();
      if (voice) {
        utterance.voice = voice;
      }

      const speedKey = rate as keyof typeof SPEECH_RATES;
      utterance.rate = SPEECH_RATES[speedKey] || 0.92;
      utterance.pitch = 1.05;

      utterance.onend = () => resolve();
      utterance.onerror = () => resolve();

      // Timeout fallback
      const timeout = setTimeout(() => resolve(), 5000);
      utterance.onend = () => {
        clearTimeout(timeout);
        resolve();
      };

      this.currentUtterance = utterance;
      synth.speak(utterance);
    });
  }

  /**
   * Speak using ElevenLabs API
   */
  async speakElevenLabs(text: string): Promise<void> {
    const apiKey = this.settings.elApiKey;
    if (!apiKey) {
      console.warn("ElevenLabs API key not set, falling back to browser voice");
      return this.speakBrowser(text, this.settings.speed);
    }

    const voiceId = this.settings.elVoiceId || "EXAVITQu4vr4xnSDxMaL";

    try {
      const response = await fetch(
        `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}/stream`,
        {
          method: "POST",
          headers: {
            "xi-api-key": apiKey,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text,
            model_id: "eleven_turbo_v2",
            voice_settings: {
              stability: 0.5,
              similarity_boost: 0.8,
              style: 0.2,
              use_speaker_boost: true,
            },
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`ElevenLabs API error: ${response.statusText}`);
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);

      return new Promise((resolve) => {
        audio.onended = () => {
          URL.revokeObjectURL(url);
          resolve();
        };
        audio.onerror = () => {
          URL.revokeObjectURL(url);
          resolve();
        };
        audio.play().catch(() => {
          URL.revokeObjectURL(url);
          resolve();
        });
      });
    } catch (error) {
      console.error("ElevenLabs error:", error);
      // Fallback to browser voice
      return this.speakBrowser(text, this.settings.speed);
    }
  }

  /**
   * Main speak method - routes to appropriate engine
   */
  async speak(text: string): Promise<void> {
    if (!text) return;

    if (this.settings.voiceEngine === "elevenlabs") {
      return this.speakElevenLabs(text);
    } else {
      return this.speakBrowser(text, this.settings.speed);
    }
  }

  /**
   * Cancel current speech
   */
  cancel(): void {
    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
  }

  /**
   * Convert a number to words (0-12)
   */
  numberToWord(n: number): string {
    if (n >= 0 && n < NUM_WORDS.length) {
      return NUM_WORDS[n];
    }
    return n.toString();
  }

  /**
   * Get a random cheer phrase
   */
  getRandomCheer(): string {
    return CHEERS[Math.floor(Math.random() * CHEERS.length)];
  }

  /**
   * Update settings
   */
  updateSettings(newSettings: Partial<Settings>): void {
    this.settings = { ...this.settings, ...newSettings };
  }

  /**
   * Test the voice settings
   */
  async testVoice(): Promise<void> {
    const testText = "Hello! Testing voice settings.";
    await this.speak(testText);
  }
}
