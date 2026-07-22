"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { ArrowLeft, Home } from "lucide-react";

export default function NotFound() {
  const pathname = usePathname();
  const isMarket = pathname?.startsWith("/market") ?? false;

  if (isMarket) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-[#faf7ee] px-6 text-center text-[#3d2f24]">
        <div className="relative mb-6">
          <div className="absolute inset-0 rounded-full bg-[#2f6b3a]/20 blur-2xl" />
          <Image
            src="/tezz_logo.png"
            alt="TEZZ MARKET"
            width={80}
            height={80}
            className="relative rounded-2xl object-contain"
          />
        </div>
        <div className="text-7xl font-black leading-none text-[#2f6b3a]">404</div>
        <h1 className="mt-3 text-xl font-bold">Страница не найдена</h1>
        <p className="mt-2 max-w-sm text-sm text-[#6b6b6b]">
          Такой страницы в TEZZ Market нет или она была перемещена.
        </p>
        <Link
          href="/market"
          className="mt-6 inline-flex items-center gap-2 rounded-xl bg-[#2f6b3a] px-6 py-3 text-sm font-bold text-[#faf7ee] transition-colors hover:bg-[#1f4f2a]"
        >
          <ArrowLeft className="h-4 w-4" />
          Вернуться в маркет
        </Link>
      </div>
    );
  }

  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden bg-slate-50 px-6 text-center">
      <div className="glow left-1/2 top-0 h-[380px] w-[380px] -translate-x-1/2 bg-brand-400/40" />
      <div className="relative mb-6">
        <div className="absolute inset-0 rounded-full bg-brand-500/20 blur-2xl" />
        <Image
          src="/tezzedu_logo.png"
          alt="TEZZ"
          width={80}
          height={80}
          className="relative rounded-2xl object-contain"
        />
      </div>
      <div className="relative text-7xl font-black leading-none text-gradient">404</div>
      <h1 className="relative mt-3 text-xl font-bold text-slate-900">
        Страница не найдена
      </h1>
      <p className="relative mt-2 max-w-sm text-sm text-slate-500">
        Такой страницы нет или она была перемещена.
      </p>
      <Link
        href="/"
        className="relative mt-6 inline-flex items-center gap-2 rounded-xl bg-brand-gradient px-6 py-3 text-sm font-semibold text-white shadow-soft transition-opacity hover:opacity-95"
      >
        <Home className="h-4 w-4" />
        На главную
      </Link>
    </div>
  );
}
