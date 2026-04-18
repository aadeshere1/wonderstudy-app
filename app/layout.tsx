import type { Metadata } from "next";
import { Fredoka, Nunito } from "next/font/google";
import { SchemaMarkup, organizationSchema } from "@/components/seo/SchemaMarkup";
import { StarsBackground } from "@/components/layout";
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
  title: "WonderStudy - Learn Math, English & Science",
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
    title: "WonderStudy",
    description: "Interactive educational games for kids",
    type: "website",
    siteName: "WonderStudy",
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
    >
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <SchemaMarkup schema={organizationSchema} />
      </head>
      <body suppressHydrationWarning className="bg-bg text-white font-body antialiased overflow-x-hidden min-h-screen">
        <StarsBackground />
        {children}
      </body>
    </html>
  );
}
