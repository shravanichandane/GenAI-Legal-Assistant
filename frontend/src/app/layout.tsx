import type { Metadata } from "next";
import { Inter, Playfair_Display, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-sans",
  subsets: ["latin"],
});

const playfair = Playfair_Display({
  variable: "--font-serif",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800", "900"],
});

const mono = JetBrains_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "LegalSight AI | Enterprise Legal Intelligence",
  description: "Production-grade contract analysis and risk detection.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${playfair.variable} ${mono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-[#F9FAFB] text-slate-900 font-sans selection:bg-slate-900 selection:text-white">
        {children}
      </body>
    </html>
  );
}
