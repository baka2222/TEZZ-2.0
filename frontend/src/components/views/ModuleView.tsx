"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowLeft, ArrowRight, CalendarClock, FileText } from "lucide-react";
import { api } from "@/lib/api";
import type { Module } from "@/lib/types";
import { EmptyState, PageError, PageLoader } from "@/components/ui";
import { formatDateTime } from "@/lib/format";

export default function ModuleView({ moduleId }: { moduleId: string }) {
  const [module, setModule] = useState<Module | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    api
      .get<Module>(`/modules/${moduleId}/`)
      .then(setModule)
      .catch(() => setError(true));
  }, [moduleId]);

  if (error) return <PageError message="Не удалось загрузить модуль" />;
  if (!module) return <PageLoader label="Загрузка модуля…" />;

  const lessons = module.lessons ?? [];

  return (
    <div>
      <Link
        href="/modules"
        className="mb-6 inline-flex items-center gap-1.5 text-sm font-medium text-slate-500 transition-colors hover:text-brand-600"
      >
        <ArrowLeft className="h-4 w-4" />
        Назад к модулям
      </Link>

      <div className="mb-8">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
          {module.title}
        </h1>
        {module.description && (
          <p className="mt-2 max-w-2xl text-slate-500">{module.description}</p>
        )}
      </div>

      <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-slate-400">
        Уроки модуля
      </h2>

      {lessons.length === 0 ? (
        <EmptyState icon={FileText} title="В этом модуле пока нет уроков" />
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {lessons.map((lesson) => (
            <Link
              key={lesson.id}
              href={`/modules/${moduleId}/lessons/${lesson.id}`}
              className="group flex flex-col rounded-2xl border border-slate-200 bg-white p-5 shadow-soft transition-all hover:-translate-y-0.5 hover:border-brand-200 hover:shadow-lg"
            >
              <div className="flex items-start gap-3">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-brand-50 text-brand-600">
                  <FileText className="h-5 w-5" />
                </div>
                <div className="min-w-0 flex-1">
                  <h3 className="font-semibold text-slate-900">{lesson.title}</h3>
                  {lesson.start_time && (
                    <p className="mt-0.5 inline-flex items-center gap-1.5 text-xs text-slate-400">
                      <CalendarClock className="h-3.5 w-3.5" />
                      {formatDateTime(lesson.start_time)}
                    </p>
                  )}
                </div>
              </div>

              {lesson.content && (
                <p className="mt-3 line-clamp-2 text-sm text-slate-500">
                  {lesson.content}
                </p>
              )}

              <div className="mt-4 flex items-center gap-1.5 text-sm font-semibold text-brand-600">
                Открыть урок
                <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
