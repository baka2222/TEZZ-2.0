"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { AlertCircle, ArrowRight, Lock, Send, User } from "lucide-react";
import { login } from "@/lib/api";
import { Spinner } from "@/components/ui";

export default function LoginView() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
      router.replace("/modules");
    } catch {
      setError("Неверный логин или пароль");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-slate-950 px-4 py-12">
      {/* Фоновое свечение */}
      <div className="glow left-[-10%] top-[-10%] h-[420px] w-[420px] bg-brand-600" />
      <div className="glow bottom-[-15%] right-[-5%] h-[380px] w-[380px] bg-accent-600" />
      <div
        className="absolute inset-0 opacity-[0.04]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,.6) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.6) 1px, transparent 1px)",
          backgroundSize: "44px 44px",
        }}
      />

      <div className="relative w-full max-w-md">
        <div className="rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl backdrop-blur-xl">
          <div className="mb-8 text-center">
            <div className="mx-auto mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-gradient text-2xl font-black text-white shadow-lg">
              T
            </div>
            <h1 className="text-2xl font-bold text-white">Добро пожаловать</h1>
            <p className="mt-1 text-sm text-slate-400">Войдите в свой аккаунт TEZZ</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <LoginInput
              icon={User}
              placeholder="Логин"
              value={username}
              onChange={setUsername}
              autoComplete="username"
            />
            <LoginInput
              icon={Lock}
              type="password"
              placeholder="Пароль"
              value={password}
              onChange={setPassword}
              autoComplete="current-password"
            />

            {error && (
              <div className="flex items-center gap-2 rounded-xl bg-rose-500/10 px-4 py-3 text-sm text-rose-300">
                <AlertCircle className="h-4 w-4 shrink-0" />
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="group flex w-full items-center justify-center gap-2 rounded-xl bg-brand-gradient px-4 py-3 text-sm font-semibold text-white shadow-lg transition-opacity hover:opacity-95 disabled:opacity-60"
            >
              {loading ? (
                <Spinner className="h-4 w-4" />
              ) : (
                <>
                  Войти
                  <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
                </>
              )}
            </button>
          </form>

          <div className="mt-8 border-t border-white/10 pt-6 text-center">
            <p className="text-sm text-slate-400">Нужна помощь с доступом?</p>
            <a
              href="https://t.me/isbakks"
              target="_blank"
              rel="noopener noreferrer"
              className="mt-2 inline-flex items-center gap-2 text-sm font-medium text-brand-300 hover:text-brand-200"
            >
              <Send className="h-4 w-4" />
              Написать в Telegram: @isbakks
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

function LoginInput({
  icon: Icon,
  type = "text",
  placeholder,
  value,
  onChange,
  autoComplete,
}: {
  icon: typeof User;
  type?: string;
  placeholder: string;
  value: string;
  onChange: (v: string) => void;
  autoComplete?: string;
}) {
  return (
    <div className="relative">
      <Icon className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
      <input
        type={type}
        placeholder={placeholder}
        value={value}
        autoComplete={autoComplete}
        onChange={(e) => onChange(e.target.value)}
        className="w-full rounded-xl border border-white/10 bg-white/5 py-3 pl-11 pr-4 text-sm text-white placeholder-slate-500 outline-none transition-colors focus:border-brand-400 focus:bg-white/10 focus:ring-2 focus:ring-brand-500/30"
      />
    </div>
  );
}
