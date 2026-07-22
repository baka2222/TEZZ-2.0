"use client";

import { useEffect, useMemo, useState } from "react";
import { Award, BarChart3, ClipboardList, TrendingUp } from "lucide-react";
import { api } from "@/lib/api";
import type { Module } from "@/lib/types";
import { EmptyState, PageError, PageHeader, PageLoader } from "@/components/ui";
import { formatDate } from "@/lib/format";

function markTone(v: number): string {
  if (v >= 80) return "text-emerald-600";
  if (v >= 60) return "text-amber-600";
  return "text-rose-600";
}

function markBadge(v: number): string {
  if (v >= 80) return "bg-emerald-50 text-emerald-700";
  if (v >= 60) return "bg-amber-50 text-amber-700";
  return "bg-rose-50 text-rose-700";
}

export default function DiaryView() {
  const [modules, setModules] = useState<Module[] | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    api
      .get<Module[]>("/modules/")
      .then(setModules)
      .catch(() => setError(true));
  }, []);

  const stats = useMemo(() => {
    let total = 0;
    let completed = 0;
    let sum = 0;
    let highest = 0;
    for (const m of modules ?? []) {
      for (const l of m.lessons ?? []) {
        total++;
        if (l.student_mark != null) {
          completed++;
          sum += l.student_mark;
          highest = Math.max(highest, l.student_mark);
        }
      }
    }
    return {
      average: completed > 0 ? sum / completed : 0,
      completed,
      total,
      highest,
    };
  }, [modules]);

  if (error) return <PageError message="Не удалось загрузить дневник" />;
  if (!modules) return <PageLoader label="Загрузка дневника…" />;

  return (
    <div>
      <PageHeader
        icon={ClipboardList}
        title="Дневник успеваемости"
        subtitle="Обзор вашей успеваемости по всем модулям"
      />

      {/* Статистика */}
      <div className="mb-8 grid gap-4 sm:grid-cols-3">
        <StatCard icon={BarChart3} tone="brand" value={stats.average.toFixed(1)} label="Средний балл" hint="из 100 возможных" />
        <StatCard
          icon={Award}
          tone="emerald"
          value={`${stats.completed}/${stats.total}`}
          label="Выполнено уроков"
          hint={
            stats.total > 0
              ? `${Math.round((stats.completed / stats.total) * 100)}% завершено`
              : "Нет уроков"
          }
        />
        <StatCard icon={TrendingUp} tone="amber" value={stats.highest} label="Лучшая оценка" hint="максимальный балл" />
      </div>

      {/* Таблица по модулям */}
      <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-slate-400">
        Детализация по модулям
      </h2>

      {modules.length === 0 ? (
        <EmptyState icon={ClipboardList} title="У вас пока нет модулей с оценками" />
      ) : (
        <div className="mb-10 space-y-3">
          {modules.map((m) => {
            const lessons = m.lessons ?? [];
            const done = lessons.filter((l) => l.student_mark != null);
            const avg =
              done.length > 0
                ? done.reduce((a, l) => a + (l.student_mark ?? 0), 0) / done.length
                : 0;
            const best = done.reduce((a, l) => Math.max(a, l.student_mark ?? 0), 0);
            const progress = lessons.length > 0 ? (done.length / lessons.length) * 100 : 0;

            return (
              <div
                key={m.id}
                className="grid items-center gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-soft sm:grid-cols-[1fr_auto_auto] sm:gap-6"
              >
                <div className="min-w-0">
                  <h3 className="font-semibold text-slate-900">{m.title}</h3>
                  {m.description && (
                    <p className="truncate text-sm text-slate-400">{m.description}</p>
                  )}
                  <div className="mt-3 flex items-center gap-3">
                    <div className="h-2 w-full max-w-xs overflow-hidden rounded-full bg-slate-100">
                      <div
                        className="h-full rounded-full bg-brand-gradient"
                        style={{ width: `${progress}%` }}
                      />
                    </div>
                    <span className="shrink-0 text-xs font-medium text-slate-500">
                      {done.length}/{lessons.length}
                    </span>
                  </div>
                </div>

                <div className="text-center">
                  <div className={`text-xl font-bold ${avg > 0 ? markTone(avg) : "text-slate-300"}`}>
                    {avg > 0 ? avg.toFixed(1) : "—"}
                  </div>
                  <div className="text-xs text-slate-400">средний</div>
                </div>

                <div className="text-center">
                  <div className="text-xl font-bold text-slate-700">
                    {best > 0 ? best : "—"}
                  </div>
                  <div className="text-xs text-slate-400">лучший</div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Детализация по урокам */}
      <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-slate-400">
        Детализация по урокам
      </h2>

      <div className="space-y-8">
        {modules.map((m) => (
          <div key={m.id}>
            <h3 className="mb-3 font-semibold text-slate-800">{m.title}</h3>
            {(m.lessons ?? []).length === 0 ? (
              <p className="text-sm text-slate-400">В этом модуле нет уроков</p>
            ) : (
              <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                {m.lessons.map((l) => (
                  <div
                    key={l.id}
                    className="flex flex-col rounded-2xl border border-slate-200 bg-white p-4 shadow-soft"
                  >
                    <div className="mb-2 flex items-start justify-between gap-3">
                      <h4 className="font-medium text-slate-900">{l.title}</h4>
                      {l.student_mark != null ? (
                        <span
                          className={`shrink-0 rounded-lg px-2 py-0.5 text-sm font-bold ${markBadge(l.student_mark)}`}
                        >
                          {l.student_mark}
                        </span>
                      ) : (
                        <span className="shrink-0 rounded-lg bg-slate-100 px-2 py-0.5 text-sm font-bold text-slate-400">
                          —
                        </span>
                      )}
                    </div>
                    {l.content && (
                      <p className="line-clamp-2 text-sm text-slate-500">{l.content}</p>
                    )}
                    <div className="mt-3 flex items-center justify-between border-t border-slate-100 pt-3 text-xs text-slate-400">
                      <span>Создан: {formatDate(l.created_at)}</span>
                      <span>Обновлён: {formatDate(l.updated_at)}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function StatCard({
  icon: Icon,
  tone,
  value,
  label,
  hint,
}: {
  icon: typeof Award;
  tone: "brand" | "emerald" | "amber";
  value: string | number;
  label: string;
  hint: string;
}) {
  const tones = {
    brand: "bg-brand-50 text-brand-600",
    emerald: "bg-emerald-50 text-emerald-600",
    amber: "bg-amber-50 text-amber-600",
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
