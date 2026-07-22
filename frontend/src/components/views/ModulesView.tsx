"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight, BookOpen, Layers, PlayCircle } from "lucide-react";
import { api } from "@/lib/api";
import type { Module } from "@/lib/types";
import { EmptyState, PageError, PageHeader, PageLoader } from "@/components/ui";

export default function ModulesView() {
  const [modules, setModules] = useState<Module[] | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    api
      .get<Module[]>("/modules/")
      .then(setModules)
      .catch(() => setError(true));
  }, []);

  if (error) return <PageError message="Не удалось загрузить модули" />;
  if (!modules) return <PageLoader label="Загрузка модулей…" />;

  return (
    <div>
      <PageHeader
        icon={Layers}
        title="Модули обучения"
        subtitle="Выберите модуль, чтобы посмотреть уроки"
      />

      {modules.length === 0 ? (
        <EmptyState icon={BookOpen} title="Модули пока не добавлены" />
      ) : (
        <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
          {modules.map((m) => {
            const count = m.lessons?.length ?? 0;
            return (
              <Link
                key={m.id}
                href={`/modules/${m.id}`}
                className="group flex flex-col rounded-2xl border border-slate-200 bg-white p-6 shadow-soft transition-all hover:-translate-y-0.5 hover:border-brand-200 hover:shadow-lg"
              >
                <div className="mb-4 flex items-center justify-between">
                  <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-brand-50 text-brand-600 transition-colors group-hover:bg-brand-gradient group-hover:text-white">
                    <BookOpen className="h-5 w-5" />
                  </div>
                  <span className="inline-flex items-center gap-1.5 rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-500">
                    <PlayCircle className="h-3.5 w-3.5" />
                    {count} {pluralLessons(count)}
                  </span>
                </div>

                <h2 className="text-lg font-semibold text-slate-900">{m.title}</h2>
                {m.description && (
                  <p className="mt-2 line-clamp-3 text-sm text-slate-500">
                    {m.description}
                  </p>
                )}

                <div className="mt-5 flex items-center gap-1.5 text-sm font-semibold text-brand-600">
                  Открыть модуль
                  <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}

function pluralLessons(n: number): string {
  const mod10 = n % 10;
  const mod100 = n % 100;
  if (mod10 === 1 && mod100 !== 11) return "урок";
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) return "урока";
  return "уроков";
}
