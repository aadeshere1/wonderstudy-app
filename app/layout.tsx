import type { Metadata } from "next";
import { Fredoka, Nunito } from "next/font/google";
import Script from "next/script";
import { SchemaMarkup, organizationSchema } from "@/components/seo/SchemaMarkup";
import { StarsBackground } from "@/components/layout";
import { AuthProvider } from "@/contexts/AuthContext";
import { ThemeProvider } from "@/contexts/ThemeContext";
import { GamificationProvider } from "@/contexts/GamificationContext";
import BadgeToast from "@/components/gamification/BadgeToast";
import LevelUpModal from "@/components/gamification/LevelUpModal";
import "./globals.css";

const fredoka = Fredoka({
  variable: "--font-fredoka-one",
  subsets: ["latin"],
});

const nunito = Nunito({
  variable: "--font-nunito",
  subsets: ["latin"],
  weight: ["400", "600", "700", "800", "900"],
});

export const metadata: Metadata = {
  title: "Sikshya - Learn Math, English & Science",
  description:
    "Interactive games for kids to practice and memorize mathematics, English, and science fundamentals. Classes 1-10.",
  keywords: [
    "kids learning",
    "math games",
    "english games",
    "science games",
    "educational games",
    "multiplication",
    "vocabulary",
    "spelling",
  ],
  robots: "index, follow",
  openGraph: {
    title: "Sikshya",
    description: "Interactive educational games for kids",
    type: "website",
    siteName: "Sikshya",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${fredoka.variable} ${nunito.variable} scroll-smooth`}
      suppressHydrationWarning
    >
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <SchemaMarkup schema={organizationSchema} />
        {/* Anti-flash: apply saved theme before React hydrates */}
        <script dangerouslySetInnerHTML={{ __html: `
          try {
            var t = localStorage.getItem('ws_theme') || 'light';
            document.documentElement.setAttribute('data-theme', t);
          } catch(e) {}
        `}} />
      </head>
      {/* Google Analytics */}
      <Script
        src="https://www.googletagmanager.com/gtag/js?id=G-22B81SDWJQ"
        strategy="afterInteractive"
      />
      <Script id="google-analytics" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'G-22B81SDWJQ');
        `}
      </Script>
      <body suppressHydrationWarning className="font-body antialiased overflow-x-hidden min-h-screen" style={{ background: 'var(--ws-bg)', color: 'var(--ws-text)' }}>
        <StarsBackground />
        <ThemeProvider>
          <AuthProvider>
            <GamificationProvider>
              <BadgeToast />
              <LevelUpModal />
              {children}
            </GamificationProvider>
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
