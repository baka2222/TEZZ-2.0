"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  CalendarPlus,
  CheckCircle2,
  Clock,
  ExternalLink,
  FileUp,
  PenLine,
  Save,
  Upload,
  Users,
  XCircle,
} from "lucide-react";
import { api, ApiError } from "@/lib/api";
import type { Lesson, MarkRow, Profile } from "@/lib/types";
import { EmptyState, PageError, PageLoader, Spinner } from "@/components/ui";
import { formatDateTime } from "@/lib/format";

export default function LessonView({
  moduleId,
  lessonId,
}: {
  moduleId: string;
  lessonId: string;
}) {
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [user, setUser] = useState<Profile | null>(null);
  const [students, setStudents] = useState<MarkRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState<{ ok: boolean; text: string } | null>(null);

  const flash = (ok: boolean, text: string, ms = 3000) => {
    setStatus({ ok, text });
    setTimeout(() => setStatus(null), ms);
  };

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        setLoading(true);
        const [lessonRes, userRes] = await Promise.all([
          api.get<Lesson>(`/lessons/${lessonId}/`),
          api.get<Profile>("/profile/"),
        ]);
        if (!active) return;
        setLesson(lessonRes);
        setUser(userRes);

        if (userRes.role === "teacher") {
          const rows = await api.get<MarkRow[]>(`/lessons/${lessonId}/students/`);
          if (active) setStudents(rows);
        } else {
          try {
            const rows = await api.get<MarkRow[]>(`/marks/${lessonId}/`);
            if (active) setStudents(rows);
          } catch {
            if (active) setStudents([]);
          }
        }
      } catch {
        if (active) setError(true);
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => {
      active = false;
    };
  }, [lessonId]);

  const handleScoreUpdate = async (row: MarkRow) => {
    if (!row.mark_id) {
      flash(false, "Нет записи оценки — создайте её в админке", 4000);
      return;
    }
    const raw = row.mark ?? row.score ?? "";
    const payload = { score: raw === "" ? null : Number(raw) };
    try {
      await api.patch(`/marks/${row.mark_id}/update/`, payload);
      setStudents((prev) =>
        prev.map((s) => (s.mark_id === row.mark_id ? { ...s, mark: payload.score } : s)),
      );
      flash(true, "Оценка обновлена");
    } catch {
      flash(false, "Ошибка обновления оценки", 4000);
    }
  };

  const handleFileUpload = async () => {
    if (!file) return;
    const markId = students[0]?.id;
    if (!markId) {
      flash(false, "Сначала учитель должен создать оценку", 4000);
      return;
    }
    try {
      setUploading(true);
      const form = new FormData();
      form.append("answer", file);
      await api.patch(`/marks/${markId}/update/`, form);
      flash(true, "Файл успешно загружен");
      setFile(null);
    } catch (e) {
      const msg = e instanceof ApiError ? "Ошибка загрузки файла" : "Ошибка загрузки файла";
      flash(false, msg, 4000);
    } finally {
      setUploading(false);
    }
  };

  if (error) return <PageError message="Не удалось загрузить урок" />;
  if (loading || !lesson) return <PageLoader label="Загрузка урока…" />;

  const isTeacher = user?.role === "teacher";
  const studentScore = students[0]?.score;

  return (
    <div>
      <Link
        href={`/modules/${moduleId}`}
        className="mb-6 inline-flex items-center gap-1.5 text-sm font-medium text-slate-500 transition-colors hover:text-brand-600"
      >
        <ArrowLeft className="h-4 w-4" />
        Назад к модулю
      </Link>

      {/* Шапка урока */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-soft">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          {lesson.title}
        </h1>

        <div className="mt-4 flex flex-wrap gap-x-6 gap-y-2 text-sm text-slate-500">
          <Meta icon={CalendarPlus} label="Создан" value={formatDateTime(lesson.created_at)} />
          <Meta icon={PenLine} label="Обновлён" value={formatDateTime(lesson.updated_at)} />
          {lesson.start_time && (
            <Meta icon={Clock} label="Начало" value={formatDateTime(lesson.start_time)} />
          )}
          {lesson.end_time && (
            <Meta icon={Clock} label="Окончание" value={formatDateTime(lesson.end_time)} />
          )}
        </div>

        {lesson.description && (
          <p className="mt-4 text-slate-600">{lesson.description}</p>
        )}

        {lesson.content && (
          <div className="mt-5 rounded-xl bg-slate-50 p-4">
            <h3 className="mb-2 text-sm font-semibold text-slate-700">
              Домашняя работа
            </h3>
            <div className="whitespace-pre-wrap text-sm text-slate-600">
              {lesson.content}
            </div>
          </div>
        )}
      </div>

      {/* Тост статуса */}
      {status && (
        <div
          className={`mt-4 flex items-center gap-2 rounded-xl px-4 py-3 text-sm font-medium ${
            status.ok
              ? "bg-emerald-50 text-emerald-700"
              : "bg-rose-50 text-rose-700"
          }`}
        >
          {status.ok ? (
            <CheckCircle2 className="h-4 w-4" />
          ) : (
            <XCircle className="h-4 w-4" />
          )}
          {status.text}
        </div>
      )}

      {/* Основной блок */}
      <div className="mt-8">
        {isTeacher ? (
          <TeacherView
            students={students}
            setStudents={setStudents}
            onSave={handleScoreUpdate}
          />
        ) : (
          <StudentView
            score={studentScore}
            file={file}
            setFile={setFile}
            uploading={uploading}
            onUpload={handleFileUpload}
          />
        )}
      </div>
    </div>
  );
}

function Meta({
  icon: Icon,
  label,
  value,
}: {
  icon: typeof Clock;
  label: string;
  value: string;
}) {
  return (
    <span className="inline-flex items-center gap-1.5">
      <Icon className="h-4 w-4 text-slate-400" />
      <span className="text-slate-400">{label}:</span>
      <span className="font-medium text-slate-600">{value}</span>
    </span>
  );
}

/* ------------------------------ Teacher --------------------------- */

function TeacherView({
  students,
  setStudents,
  onSave,
}: {
  students: MarkRow[];
  setStudents: React.Dispatch<React.SetStateAction<MarkRow[]>>;
  onSave: (row: MarkRow) => void;
}) {
  return (
    <section>
      <h2 className="mb-4 flex items-center gap-2 text-lg font-semibold text-slate-900">
        <Users className="h-5 w-5 text-brand-600" />
        Студенты и оценки
      </h2>

      {students.length === 0 ? (
        <EmptyState icon={Users} title="На этот урок ещё не записаны студенты" />
      ) : (
        <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-soft">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-400">
                <th className="px-4 py-3 font-medium">Студент</th>
                <th className="px-4 py-3 font-medium">Оценка</th>
                <th className="px-4 py-3 font-medium">Работа</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {students.map((s) => {
                const value = (s.mark ?? s.score) ?? "";
                return (
                  <tr key={s.id} className="hover:bg-slate-50/60">
                    <td className="px-4 py-3 font-medium text-slate-800">
                      {s.first_name || `Студент #${s.id}`}
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <input
                          type="text"
                          inputMode="numeric"
                          value={value ?? ""}
                          onChange={(e) => {
                            const v = e.target.value.replace(/\D+/g, "");
                            setStudents((prev) =>
                              prev.map((row) =>
                                row.id === s.id
                                  ? { ...row, mark: v === "" ? null : Number(v), score: v === "" ? null : Number(v) }
                                  : row,
                              ),
                            );
                          }}
                          placeholder="0–100"
                          className="w-20 rounded-lg border border-slate-200 px-3 py-1.5 text-sm outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100"
                        />
                        <button
                          onClick={() => onSave(s)}
                          disabled={!s.mark_id}
                          title={
                            s.mark_id
                              ? "Сохранить оценку"
                              : "Нет записи оценки (mark)"
                          }
                          className="inline-flex items-center gap-1.5 rounded-lg bg-brand-600 px-3 py-1.5 text-xs font-semibold text-white transition-colors hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-40"
                        >
                          <Save className="h-3.5 w-3.5" />
                          Сохранить
                        </button>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      {s.answer_url ? (
                        <a
                          href={s.answer_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1.5 text-brand-600 hover:underline"
                        >
                          Посмотреть
                          <ExternalLink className="h-3.5 w-3.5" />
                        </a>
                      ) : (
                        <span className="text-slate-300">—</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

/* ------------------------------ Student --------------------------- */

function StudentView({
  score,
  file,
  setFile,
  uploading,
  onUpload,
}: {
  score?: number | null;
  file: File | null;
  setFile: (f: File | null) => void;
  uploading: boolean;
  onUpload: () => void;
}) {
  return (
    <section className="grid gap-6 md:grid-cols-2">
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-soft">
        <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">
          Ваша оценка
        </h3>
        {score ? (
          <div className="mt-4 flex items-end gap-2">
            <span className="text-5xl font-bold text-gradient">{score}</span>
            <span className="mb-1.5 text-sm text-slate-400">баллов</span>
          </div>
        ) : (
          <p className="mt-4 text-sm text-slate-500">Оценка ещё не выставлена</p>
        )}
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-soft">
        <h3 className="mb-3 flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-slate-400">
          <Upload className="h-4 w-4" />
          Загрузить ответ
        </h3>

        <label className="flex cursor-pointer flex-col items-center justify-center gap-2 rounded-xl border-2 border-dashed border-slate-200 px-4 py-8 text-center transition-colors hover:border-brand-300 hover:bg-brand-50/40">
          <FileUp className="h-6 w-6 text-slate-400" />
          <span className="text-sm font-medium text-slate-600">
            {file ? file.name : "Выберите файл"}
          </span>
          <input
            type="file"
            className="hidden"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          />
        </label>

        <button
          onClick={onUpload}
          disabled={!file || uploading}
          className="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {uploading ? <Spinner className="h-4 w-4" /> : <Upload className="h-4 w-4" />}
          {uploading ? "Загрузка…" : "Загрузить"}
        </button>
      </div>
    </section>
  );
}
