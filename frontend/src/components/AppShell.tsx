"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BookOpen,
  CalendarDays,
  ClipboardList,
  LogOut,
  Menu,
  User,
  X,
  type LucideIcon,
} from "lucide-react";
import { logout } from "@/lib/api";

interface NavItem {
  href: string;
  label: string;
  icon: LucideIcon;
}

const NAV: NavItem[] = [
  { href: "/profile", label: "Профиль", icon: User },
  { href: "/schedule", label: "Расписание", icon: CalendarDays },
  { href: "/diary", label: "Дневник", icon: ClipboardList },
  { href: "/modules", label: "Модули", icon: BookOpen },
];

function BrandMark() {
  return (
    <Link href="/modules" className="flex items-center gap-3">
      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-gradient text-lg font-black text-white shadow-soft">
        T
      </div>
      <div className="leading-tight">
        <div className="text-base font-bold tracking-wide text-white">TEZZ</div>
        <div className="text-[11px] font-medium uppercase tracking-[0.2em] text-slate-400">
          Courses
        </div>
      </div>
    </Link>
  );
}

function NavLinks({ onNavigate }: { onNavigate?: () => void }) {
  const pathname = usePathname();
  return (
    <nav className="flex flex-1 flex-col gap-1 px-3">
      {NAV.map(({ href, label, icon: Icon }) => {
        const active = pathname === href || pathname.startsWith(`${href}/`);
        return (
          <Link
            key={href}
            href={href}
            onClick={onNavigate}
            className={`group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors ${
              active
                ? "bg-white/10 text-white"
                : "text-slate-400 hover:bg-white/5 hover:text-white"
            }`}
          >
            {active && (
              <span className="absolute left-0 top-1/2 h-6 -translate-y-1/2 rounded-r-full bg-brand-400 [width:3px]" />
            )}
            <Icon
              className={`h-5 w-5 shrink-0 ${active ? "text-brand-300" : "text-slate-500 group-hover:text-slate-300"}`}
            />
            <span>{label}</span>
          </Link>
        );
      })}
    </nav>
  );
}

function SidebarInner({ onNavigate }: { onNavigate?: () => void }) {
  return (
    <div className="flex h-full flex-col bg-slate-900">
      <div className="flex items-center px-5 py-5">
        <BrandMark />
      </div>
      <div className="mt-2 flex-1">
        <NavLinks onNavigate={onNavigate} />
      </div>
      <div className="border-t border-white/5 p-3">
        <button
          onClick={logout}
          className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-slate-400 transition-colors hover:bg-rose-500/10 hover:text-rose-300"
        >
          <LogOut className="h-5 w-5" />
          Выйти
        </button>
      </div>
    </div>
  );
}

export default function AppShell({ children }: { children: React.ReactNode }) {
  const [mobileOpen, setMobileOpen] = useState(false);

  // Блокируем прокрутку body при открытом drawer
  useEffect(() => {
    document.body.style.overflow = mobileOpen ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [mobileOpen]);

  return (
    <div className="min-h-screen lg:pl-64">
      {/* Десктопный сайдбар */}
      <aside className="fixed inset-y-0 left-0 z-40 hidden w-64 lg:block">
        <SidebarInner />
      </aside>

      {/* Мобильная шапка */}
      <header className="sticky top-0 z-30 flex items-center gap-3 border-b border-slate-200 bg-white/80 px-4 py-3 backdrop-blur lg:hidden">
        <button
          onClick={() => setMobileOpen(true)}
          aria-label="Открыть меню"
          className="flex h-10 w-10 items-center justify-center rounded-xl text-slate-600 hover:bg-slate-100"
        >
          <Menu className="h-5 w-5" />
        </button>
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-gradient text-sm font-black text-white">
            T
          </div>
          <span className="font-bold tracking-wide text-slate-900">TEZZ</span>
        </div>
      </header>

      {/* Мобильный drawer */}
      {mobileOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div
            className="absolute inset-0 bg-slate-900/50 backdrop-blur-sm"
            onClick={() => setMobileOpen(false)}
          />
          <div className="absolute inset-y-0 left-0 w-72 max-w-[85%] shadow-2xl">
            <button
              onClick={() => setMobileOpen(false)}
              aria-label="Закрыть меню"
              className="absolute right-3 top-4 z-10 flex h-9 w-9 items-center justify-center rounded-lg text-slate-400 hover:bg-white/10 hover:text-white"
            >
              <X className="h-5 w-5" />
            </button>
            <SidebarInner onNavigate={() => setMobileOpen(false)} />
          </div>
        </div>
      )}

      {/* Контент */}
      <main className="mx-auto w-full max-w-6xl px-4 py-8 sm:px-6 lg:px-10">
        {children}
      </main>
    </div>
  );
}
