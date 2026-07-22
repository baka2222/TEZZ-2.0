import type { NextConfig } from "next";

// В деве Next не знает про Django — проксируем /api на бэкенд.
// В проде фронт и бэкенд стоят за одним хостом (nginx), rewrites не мешают.
const API_ORIGIN = process.env.NEXT_PUBLIC_API_ORIGIN ?? "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  reactCompiler: true,
  // Компактный self-contained сервер для Docker (node .next/standalone/server.js)
  output: "standalone",
  async rewrites() {
    return [
      { source: "/api/:path*", destination: `${API_ORIGIN}/api/:path*` },
      // медиа-файлы Django (ответы студентов и т.п.)
      { source: "/media/:path*", destination: `${API_ORIGIN}/media/:path*` },
    ];
  },
};

export default nextConfig;
