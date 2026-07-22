"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, MessageCircle, Send, User, XCircle } from "lucide-react";
import { api } from "@/lib/api";
import type { Profile } from "@/lib/types";
import { PageHeader, PageLoader, Spinner } from "@/components/ui";

export default function ProfileView() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [saving, setSaving] = useState(false);
  const [status, setStatus] = useState<{ ok: boolean; text: string } | null>(null);

  useEffect(() => {
    api
      .get<Profile>("/profile/")
      .then(setProfile)
      .catch(() => {});
  }, []);

  const handleSave = async () => {
    if (!profile) return;
    setSaving(true);
    setStatus(null);
    try {
      const updated = await api.patch<Profile>("/profile/", {
        first_name: profile.first_name,
        telegram: profile.telegram,
        discord: profile.discord,
      });
      setProfile(updated);
      setStatus({ ok: true, text: "Профиль успешно обновлён" });
    } catch {
      setStatus({ ok: false, text: "Ошибка сохранения" });
    } finally {
      setSaving(false);
      setTimeout(() => setStatus(null), 2500);
    }
  };

  if (!profile) return <PageLoader label="Загрузка профиля…" />;

  const initial = (profile.first_name || "?").trim().charAt(0).toUpperCase();

  return (
    <div className="mx-auto max-w-2xl">
      <PageHeader title="Профиль" subtitle="Управление вашими данными" />

      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-soft">
        {/* Верхняя полоса с аватаром */}
        <div className="flex items-center gap-4 border-b border-slate-100 bg-gradient-to-br from-brand-50 to-white px-6 py-6">
          <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-brand-gradient text-2xl font-bold text-white shadow-soft">
            {initial}
          </div>
          <div>
            <div className="text-lg font-semibold text-slate-900">
              {profile.first_name || "Без имени"}
            </div>
            {profile.role && (
              <span className="mt-1 inline-block rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium capitalize text-slate-500">
                {profile.role === "teacher" ? "Преподаватель" : "Студент"}
              </span>
            )}
          </div>
        </div>

        <div className="space-y-5 p-6">
          <Field
            icon={User}
            label="Имя"
            value={profile.first_name ?? ""}
            onChange={(v) => setProfile({ ...profile, first_name: v })}
          />
          <Field
            icon={Send}
            label="Telegram"
            placeholder="@username"
            value={profile.telegram ?? ""}
            onChange={(v) => setProfile({ ...profile, telegram: v })}
          />
          <Field
            icon={MessageCircle}
            label="Discord"
            placeholder="username#1234"
            value={profile.discord ?? ""}
            onChange={(v) => setProfile({ ...profile, discord: v })}
          />

          <div className="flex items-center gap-4 pt-2">
            <button
              onClick={handleSave}
              disabled={saving}
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-brand-700 disabled:opacity-50"
            >
              {saving && <Spinner className="h-4 w-4" />}
              Сохранить изменения
            </button>

            {status && (
              <span
                className={`inline-flex items-center gap-1.5 text-sm font-medium ${
                  status.ok ? "text-emerald-600" : "text-rose-600"
                }`}
              >
                {status.ok ? (
                  <CheckCircle2 className="h-4 w-4" />
                ) : (
                  <XCircle className="h-4 w-4" />
                )}
                {status.text}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function Field({
  icon: Icon,
  label,
  value,
  onChange,
  placeholder,
}: {
  icon: typeof User;
  label: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
}) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-sm font-medium text-slate-600">{label}</span>
      <div className="relative">
        <Icon className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
        <input
          value={value}
          placeholder={placeholder}
          onChange={(e) => onChange(e.target.value)}
          className="w-full rounded-xl border border-slate-200 py-2.5 pl-10 pr-3 text-sm outline-none transition-colors focus:border-brand-400 focus:ring-2 focus:ring-brand-100"
        />
      </div>
    </label>
  );
}
