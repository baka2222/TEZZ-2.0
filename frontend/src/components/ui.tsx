import { AlertTriangle, type LucideIcon } from "lucide-react";

export function Spinner({ className = "" }: { className?: string }) {
  return (
    <span
      className={`inline-block animate-spin rounded-full border-2 border-current border-t-transparent ${className}`}
      role="status"
      aria-label="Загрузка"
    />
  );
}

/** Полноэкранное состояние загрузки для страниц. */
export function PageLoader({ label = "Загрузка…" }: { label?: string }) {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 text-slate-500">
      <Spinner className="h-8 w-8 text-brand-600" />
      <p className="text-sm font-medium">{label}</p>
    </div>
  );
}

/** Ошибка загрузки страницы. */
export function PageError({
  title = "Что-то пошло не так",
  message,
}: {
  title?: string;
  message?: string;
}) {
  return (
    <div className="mx-auto flex min-h-[50vh] max-w-md flex-col items-center justify-center gap-3 text-center">
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-rose-50 text-rose-500">
        <AlertTriangle className="h-6 w-6" />
      </div>
      <h2 className="text-lg font-semibold text-slate-900">{title}</h2>
      {message && <p className="text-sm text-slate-500">{message}</p>}
    </div>
  );
}

/** Пустое состояние (нет данных). */
export function EmptyState({
  icon: Icon,
  title,
  hint,
}: {
  icon: LucideIcon;
  title: string;
  hint?: string;
}) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 rounded-2xl border border-dashed border-slate-200 bg-white/60 px-6 py-14 text-center">
      <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100 text-slate-400">
        <Icon className="h-6 w-6" />
      </div>
      <p className="font-medium text-slate-700">{title}</p>
      {hint && <p className="max-w-sm text-sm text-slate-400">{hint}</p>}
    </div>
  );
}

/** Заголовок страницы с иконкой и подзаголовком. */
export function PageHeader({
  icon: Icon,
  title,
  subtitle,
  actions,
}: {
  icon?: LucideIcon;
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
}) {
  return (
    <header className="mb-8 flex flex-wrap items-start justify-between gap-4">
      <div className="flex items-start gap-4">
        {Icon && (
          <div className="hidden h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-brand-gradient text-white shadow-soft sm:flex">
            <Icon className="h-6 w-6" />
          </div>
        )}
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
            {title}
          </h1>
          {subtitle && <p className="mt-1 text-sm text-slate-500">{subtitle}</p>}
        </div>
      </div>
      {actions}
    </header>
  );
}
