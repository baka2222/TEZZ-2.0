"use client";

import { useEffect, useMemo, useState } from "react";
import {
  BellRing,
  BookOpen,
  CalendarDays,
  CheckCheck,
  ChevronLeft,
  ChevronRight,
  Clock,
} from "lucide-react";
import { api } from "@/lib/api";
import type { Lesson, Module } from "@/lib/types";
import { EmptyState, PageError, PageHeader, PageLoader } from "@/components/ui";
import { formatTime } from "@/lib/format";

type SchedLesson = Lesson & { moduleTitle: string; moduleId: number };
type ViewMode = "day" | "week" | "month";

const WEEKDAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"];

export default function ScheduleView() {
  const [modules, setModules] = useState<Module[] | null>(null);
  const [error, setError] = useState(false);
  const [current, setCurrent] = useState(() => new Date());
  const [mode, setMode] = useState<ViewMode>("week");

  useEffect(() => {
    api
      .get<Module[]>("/modules/")
      .then(setModules)
      .catch(() => setError(true));
  }, []);

  const lessons = useMemo<SchedLesson[]>(() => {
    if (!modules) return [];
    const all: SchedLesson[] = [];
    for (const m of modules) {
      for (const l of m.lessons ?? []) {
        if (l.start_time && l.end_time) {
          all.push({ ...l, moduleTitle: m.title, moduleId: m.id });
        }
      }
    }
    return all.sort(
      (a, b) => new Date(a.start_time!).getTime() - new Date(b.start_time!).getTime(),
    );
  }, [modules]);

  const byDate = useMemo(() => {
    const map = new Map<string, SchedLesson[]>();
    for (const l of lessons) {
      const key = new Date(l.start_time!).toDateString();
      const arr = map.get(key) ?? [];
      arr.push(l);
      map.set(key, arr);
    }
    return map;
  }, [lessons]);

  if (error) return <PageError message="Не удалось загрузить расписание" />;
  if (!modules) return <PageLoader label="Загрузка расписания…" />;

  const now = new Date();
  const upcoming = lessons.filter((l) => new Date(l.start_time!) > now);
  const completed = lessons.filter((l) => new Date(l.end_time!) < now);

  const navigate = (dir: 1 | -1) => {
    const d = new Date(current);
    if (mode === "day") d.setDate(d.getDate() + dir);
    else if (mode === "week") d.setDate(d.getDate() + dir * 7);
    else d.setMonth(d.getMonth() + dir);
    setCurrent(d);
  };

  return (
    <div>
      <PageHeader
        icon={CalendarDays}
        title="Расписание уроков"
        subtitle="Планируйте своё обучение эффективно"
      />

      {/* Статистика */}
      <div className="mb-6 grid gap-4 sm:grid-cols-3">
        <StatCard icon={BookOpen} tone="brand" label="Всего уроков" value={lessons.length} hint="в расписании" />
        <StatCard icon={BellRing} tone="amber" label="Предстоящие" value={upcoming.length} hint="ближайших" />
        <StatCard icon={CheckCheck} tone="emerald" label="Завершено" value={completed.length} hint="уроков" />
      </div>

      {/* Панель управления */}
      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div className="inline-flex rounded-xl border border-slate-200 bg-white p-1 shadow-soft">
          {(["day", "week", "month"] as ViewMode[]).map((m) => (
            <button
              key={m}
              onClick={() => setMode(m)}
              className={`rounded-lg px-4 py-1.5 text-sm font-medium transition-colors ${
                mode === m
                  ? "bg-brand-600 text-white shadow-sm"
                  : "text-slate-500 hover:text-slate-800"
              }`}
            >
              {m === "day" ? "День" : m === "week" ? "Неделя" : "Месяц"}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <NavBtn onClick={() => navigate(-1)} label="Назад">
            <ChevronLeft className="h-4 w-4" />
          </NavBtn>
          <div className="min-w-[180px] text-center text-sm font-semibold capitalize text-slate-700">
            {rangeLabel(current, mode)}
          </div>
          <NavBtn onClick={() => navigate(1)} label="Вперёд">
            <ChevronRight className="h-4 w-4" />
          </NavBtn>
          <button
            onClick={() => setCurrent(new Date())}
            className="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-medium text-slate-600 shadow-soft hover:bg-slate-50"
          >
            Сегодня
          </button>
        </div>
      </div>

      {/* Виды */}
      {mode === "day" && <DayView lessons={byDate.get(current.toDateString()) ?? []} />}
      {mode === "week" && <WeekView current={current} byDate={byDate} />}
      {mode === "month" && <MonthView current={current} byDate={byDate} />}

      {/* Ближайшие уроки */}
      <section className="mt-10">
        <h3 className="mb-4 text-sm font-semibold uppercase tracking-wide text-slate-400">
          Ближайшие уроки
        </h3>
        {upcoming.length === 0 ? (
          <EmptyState icon={BellRing} title="Ближайшие уроки отсутствуют" />
        ) : (
          <div className="space-y-3">
            {upcoming.slice(0, 3).map((l) => (
              <div
                key={l.id}
                className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-soft"
              >
                <div className="flex h-14 w-14 shrink-0 flex-col items-center justify-center rounded-xl bg-brand-50 text-brand-700">
                  <span className="text-lg font-bold leading-none">
                    {new Date(l.start_time!).getDate()}
                  </span>
                  <span className="text-[11px] uppercase">
                    {new Date(l.start_time!).toLocaleDateString("ru-RU", { month: "short" })}
                  </span>
                </div>
                <div className="min-w-0 flex-1">
                  <div className="truncate font-semibold text-slate-900">{l.title}</div>
                  <div className="truncate text-sm text-slate-500">{l.moduleTitle}</div>
                </div>
                <div className="hidden items-center gap-1.5 text-sm font-medium text-slate-500 sm:flex">
                  <Clock className="h-4 w-4" />
                  {formatTime(l.start_time)}–{formatTime(l.end_time)}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

/* --------------------------- подкомпоненты ------------------------ */

function StatCard({
  icon: Icon,
  tone,
  label,
  value,
  hint,
}: {
  icon: typeof BookOpen;
  tone: "brand" | "amber" | "emerald";
  label: string;
  value: number;
  hint: string;
}) {
  const tones = {
    brand: "bg-brand-50 text-brand-600",
    amber: "bg-amber-50 text-amber-600",
    emerald: "bg-emerald-50 text-emerald-600",
  };
  return (
    <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-soft">
      <div className={`flex h-12 w-12 items-center justify-center rounded-xl ${tones[tone]}`}>
        <Icon className="h-6 w-6" />
      </div>
      <div>
        <div className="text-2xl font-bold text-slate-900">{value}</div>
        <div className="text-sm font-medium text-slate-500">{label}</div>
        <div className="text-xs text-slate-400">{hint}</div>
      </div>
    </div>
  );
}

function NavBtn({
  onClick,
  label,
  children,
}: {
  onClick: () => void;
  label: string;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      aria-label={label}
      className="flex h-9 w-9 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-600 shadow-soft hover:bg-slate-50"
    >
      {children}
    </button>
  );
}

function lessonState(l: SchedLesson): "passed" | "ongoing" | "upcoming" {
  const now = new Date();
  const start = new Date(l.start_time!);
  const end = new Date(l.end_time!);
  if (end < now) return "passed";
  if (start <= now && end >= now) return "ongoing";
  return "upcoming";
}

function StatusBadge({ l }: { l: SchedLesson }) {
  const state = lessonState(l);
  const map = {
    ongoing: { text: "Сейчас", cls: "bg-emerald-100 text-emerald-700" },
    passed: { text: "Завершён", cls: "bg-slate-100 text-slate-500" },
    upcoming: { text: "Предстоит", cls: "bg-brand-100 text-brand-700" },
  };
  const { text, cls } = map[state];
  return <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${cls}`}>{text}</span>;
}

function DayView({ lessons }: { lessons: SchedLesson[] }) {
  if (lessons.length === 0) {
    return <EmptyState icon={CalendarDays} title="На этот день уроков не запланировано" />;
  }
  return (
    <div className="space-y-3">
      {lessons.map((l) => (
        <div
          key={l.id}
          className={`flex items-center gap-4 rounded-2xl border bg-white p-4 shadow-soft ${
            lessonState(l) === "ongoing" ? "border-emerald-300" : "border-slate-200"
          }`}
        >
          <div className="flex items-center gap-1.5 rounded-lg bg-slate-50 px-3 py-2 text-sm font-semibold text-slate-600">
            <Clock className="h-4 w-4 text-slate-400" />
            {formatTime(l.start_time)}–{formatTime(l.end_time)}
          </div>
          <div className="min-w-0 flex-1">
            <div className="truncate font-semibold text-slate-900">{l.title}</div>
            <div className="truncate text-sm text-slate-500">{l.moduleTitle}</div>
          </div>
          <StatusBadge l={l} />
        </div>
      ))}
    </div>
  );
}

function isToday(d: Date) {
  const t = new Date();
  return (
    d.getDate() === t.getDate() &&
    d.getMonth() === t.getMonth() &&
    d.getFullYear() === t.getFullYear()
  );
}

function weekDays(current: Date): Date[] {
  const start = new Date(current);
  const day = (start.getDay() + 6) % 7; // 0 = Monday
  start.setDate(start.getDate() - day);
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(start);
    d.setDate(start.getDate() + i);
    return d;
  });
}

function WeekView({
  current,
  byDate,
}: {
  current: Date;
  byDate: Map<string, SchedLesson[]>;
}) {
  const days = weekDays(current);
  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-7">
      {days.map((d) => {
        const dayLessons = byDate.get(d.toDateString()) ?? [];
        return (
          <div
            key={d.toDateString()}
            className={`rounded-2xl border bg-white p-3 shadow-soft ${
              isToday(d) ? "border-brand-300 ring-1 ring-brand-100" : "border-slate-200"
            }`}
          >
            <div className="mb-2 flex items-center justify-between">
              <span className="text-xs font-semibold uppercase text-slate-400">
                {d.toLocaleDateString("ru-RU", { weekday: "short" })}
              </span>
              <span
                className={`flex h-6 w-6 items-center justify-center rounded-full text-sm font-semibold ${
                  isToday(d) ? "bg-brand-600 text-white" : "text-slate-600"
                }`}
              >
                {d.getDate()}
              </span>
            </div>
            <div className="space-y-2">
              {dayLessons.length === 0 ? (
                <p className="py-2 text-center text-xs text-slate-300">Нет уроков</p>
              ) : (
                dayLessons.map((l) => (
                  <div
                    key={l.id}
                    className={`rounded-lg border-l-2 bg-slate-50 p-2 ${
                      lessonState(l) === "ongoing"
                        ? "border-emerald-400"
                        : lessonState(l) === "passed"
                          ? "border-slate-300"
                          : "border-brand-400"
                    }`}
                  >
                    <div className="text-[11px] font-medium text-slate-400">
                      {formatTime(l.start_time)}
                    </div>
                    <div className="truncate text-xs font-semibold text-slate-800">
                      {l.title}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function monthMatrix(current: Date): Date[] {
  const first = new Date(current.getFullYear(), current.getMonth(), 1);
  const start = new Date(first);
  const offset = (first.getDay() + 6) % 7; // Monday-based
  start.setDate(first.getDate() - offset);
  return Array.from({ length: 42 }, (_, i) => {
    const d = new Date(start);
    d.setDate(start.getDate() + i);
    return d;
  });
}

function MonthView({
  current,
  byDate,
}: {
  current: Date;
  byDate: Map<string, SchedLesson[]>;
}) {
  const cells = monthMatrix(current);
  const month = current.getMonth();
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-soft">
      <div className="grid grid-cols-7 border-b border-slate-100 bg-slate-50 text-center text-xs font-semibold uppercase text-slate-400">
        {WEEKDAYS.map((w) => (
          <div key={w} className="py-2">
            {w}
          </div>
        ))}
      </div>
      <div className="grid grid-cols-7">
        {cells.map((d, i) => {
          const inMonth = d.getMonth() === month;
          const dayLessons = byDate.get(d.toDateString()) ?? [];
          return (
            <div
              key={i}
              className={`min-h-[92px] border-b border-r border-slate-100 p-1.5 ${
                inMonth ? "" : "bg-slate-50/50"
              }`}
            >
              <div
                className={`mb-1 flex h-6 w-6 items-center justify-center rounded-full text-xs font-semibold ${
                  isToday(d)
                    ? "bg-brand-600 text-white"
                    : inMonth
                      ? "text-slate-600"
                      : "text-slate-300"
                }`}
              >
                {d.getDate()}
              </div>
              <div className="space-y-1">
                {dayLessons.slice(0, 2).map((l) => (
                  <div
                    key={l.id}
                    title={l.title}
                    className="truncate rounded bg-brand-50 px-1.5 py-0.5 text-[10px] font-medium text-brand-700"
                  >
                    {formatTime(l.start_time)} {l.title}
                  </div>
                ))}
                {dayLessons.length > 2 && (
                  <div className="px-1.5 text-[10px] font-medium text-slate-400">
                    +{dayLessons.length - 2}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function rangeLabel(current: Date, mode: ViewMode): string {
  if (mode === "day") {
    return current.toLocaleDateString("ru-RU", {
      weekday: "long",
      day: "numeric",
      month: "long",
    });
  }
  if (mode === "week") {
    const days = weekDays(current);
    const fmt = (d: Date) => d.toLocaleDateString("ru-RU", { day: "numeric", month: "short" });
    return `${fmt(days[0])} – ${fmt(days[6])}`;
  }
  return current.toLocaleDateString("ru-RU", { month: "long", year: "numeric" });
}
