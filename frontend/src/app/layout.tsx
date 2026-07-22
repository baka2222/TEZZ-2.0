import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "TEZZ — образовательная платформа",
    template: "%s · TEZZ",
  },
  description:
    "TEZZ — STEM-образование, расписание, дневник успеваемости и модули обучения.",
  // Система EduTech — по умолчанию лого tezzedu. Раздел /market переопределяет на tezz.
  icons: { icon: "/tezzedu_logo.png", apple: "/tezzedu_logo.png" },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru" className="h-full antialiased">
      <body className="min-h-full">{children}</body>
    </html>
  );
}
