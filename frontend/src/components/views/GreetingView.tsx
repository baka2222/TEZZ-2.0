import Link from "next/link";
import {
  Atom,
  Bot,
  Code2,
  GraduationCap,
  Lightbulb,
  Rocket,
  Send,
  Sigma,
  Sparkles,
  Target,
  Trophy,
  type LucideIcon,
} from "lucide-react";
import Reveal from "@/components/Reveal";

const TELEGRAM = "https://t.me/isbakks";
const INSTAGRAM =
  "https://www.instagram.com/tezz_edu?igsh=Y3ZuejIyZ296MHc5&utm_source=qr";

const COURSES: { icon: LucideIcon; title: string; description: string }[] = [
  { icon: Code2, title: "Программирование", description: "Python, JavaScript, C++ и современные фреймворки" },
  { icon: Bot, title: "Робототехника", description: "Arduino, Raspberry Pi и IoT-устройства" },
  { icon: Atom, title: "Физика", description: "Эксперименты и исследование законов вселенной" },
  { icon: Sigma, title: "Математика", description: "Алгебра, геометрия и математический анализ" },
];

const BENEFITS: { icon: LucideIcon; title: string; description: string }[] = [
  { icon: Rocket, title: "Практические проекты", description: "Реальные кейсы и проектная работа" },
  { icon: GraduationCap, title: "Эксперты индустрии", description: "Преподаватели с опытом в IT и инженерии" },
  { icon: Trophy, title: "Подготовка к олимпиадам", description: "Успешное выступление на конкурсах" },
  { icon: Lightbulb, title: "Инновации", description: "Современные технологии и методики" },
];

export default function GreetingView() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-950 text-slate-100">
      {/* Фоновые свечения */}
      <div className="glow left-[-8%] top-[-6%] h-[460px] w-[460px] bg-brand-600" />
      <div className="glow right-[-10%] top-[20%] h-[420px] w-[420px] bg-accent-600" />
      <div className="glow bottom-[-10%] left-[30%] h-[380px] w-[380px] bg-brand-500" />

      <div className="relative">
        {/* Хедер */}
        <header className="mx-auto flex max-w-6xl items-center justify-between px-6 py-6">
          <div>
            <div className="text-xl font-black tracking-wide">
              TEZZ <span className="text-gradient">STEM</span>
            </div>
            <div className="text-xs text-slate-400">Образовательный центр</div>
          </div>
          <Link
            href="/login"
            className="rounded-xl border border-white/15 bg-white/5 px-5 py-2 text-sm font-semibold text-white transition-colors hover:bg-white/10"
          >
            Войти
          </Link>
        </header>

        {/* Герой */}
        <section className="mx-auto grid max-w-6xl items-center gap-12 px-6 py-16 lg:grid-cols-2 lg:py-24">
          <Reveal>
            <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-sm text-brand-200">
              <Target className="h-4 w-4" />
              Будущее начинается здесь
            </div>
            <h1 className="text-4xl font-black leading-tight tracking-tight sm:text-5xl">
              STEM-образование
              <span className="block text-gradient">нового поколения</span>
            </h1>
            <p className="mt-5 max-w-xl text-lg text-slate-300">
              Программирование, робототехника, физика и математика для детей и
              подростков. Практические навыки, которые помогут построить успешное
              будущее в мире технологий.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <a
                href={TELEGRAM}
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-xl bg-brand-gradient px-6 py-3 text-sm font-semibold text-white shadow-lg transition-opacity hover:opacity-95"
              >
                Начать обучение
              </a>
              <a
                href={INSTAGRAM}
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-xl border border-white/15 bg-white/5 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-white/10"
              >
                Узнать больше
              </a>
            </div>
          </Reveal>

          {/* Плавающие карточки-иконки */}
          <Reveal delay={150}>
            <div className="relative mx-auto grid max-w-sm grid-cols-2 gap-5">
              {COURSES.map((c, i) => (
                <div
                  key={c.title}
                  className="animate-float rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-md"
                  style={{ animationDelay: `${i * 0.8}s` }}
                >
                  <c.icon className="h-9 w-9 text-brand-300" />
                  <div className="mt-3 text-sm font-semibold">{c.title}</div>
                </div>
              ))}
            </div>
          </Reveal>
        </section>

        {/* Направления */}
        <section className="mx-auto max-w-6xl px-6 py-16">
          <Reveal className="mb-10 text-center">
            <h2 className="text-3xl font-bold">Направления обучения</h2>
            <p className="mt-2 text-slate-400">Комплексный подход к STEM-образованию</p>
          </Reveal>
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {COURSES.map((c, i) => (
              <Reveal key={c.title} delay={i * 80}>
                <div className="h-full rounded-2xl border border-white/10 bg-white/5 p-6 transition-colors hover:border-brand-400/40 hover:bg-white/[0.07]">
                  <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-brand-gradient text-white">
                    <c.icon className="h-6 w-6" />
                  </div>
                  <h3 className="text-lg font-semibold">{c.title}</h3>
                  <p className="mt-1.5 text-sm text-slate-400">{c.description}</p>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {["Проекты", "Практика", "Поддержка"].map((t) => (
                      <span
                        key={t}
                        className="rounded-full bg-white/5 px-2.5 py-1 text-xs text-slate-300"
                      >
                        {t}
                      </span>
                    ))}
                  </div>
                </div>
              </Reveal>
            ))}
          </div>
        </section>

        {/* Преимущества */}
        <section className="mx-auto max-w-6xl px-6 py-16">
          <Reveal className="mb-10">
            <h2 className="text-3xl font-bold">Почему выбирают TEZZ STEM?</h2>
            <p className="mt-2 text-slate-400">Наши преимущества для успешного обучения</p>
          </Reveal>
          <div className="grid gap-5 sm:grid-cols-2">
            {BENEFITS.map((b, i) => (
              <Reveal key={b.title} delay={i * 80}>
                <div className="flex items-start gap-4 rounded-2xl border border-white/10 bg-white/5 p-6">
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-white/10 text-brand-300">
                    <b.icon className="h-6 w-6" />
                  </div>
                  <div>
                    <h4 className="font-semibold">{b.title}</h4>
                    <p className="mt-1 text-sm text-slate-400">{b.description}</p>
                  </div>
                </div>
              </Reveal>
            ))}
          </div>
        </section>

        {/* CTA */}
        <section className="mx-auto max-w-6xl px-6 py-16">
          <Reveal>
            <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-brand-600/30 to-accent-600/20 p-10 text-center sm:p-14">
              <Sparkles className="mx-auto mb-4 h-8 w-8 text-brand-200" />
              <h2 className="text-3xl font-bold">Готовы начать обучение?</h2>
              <p className="mt-2 text-slate-300">
                Присоединяйтесь к TEZZ STEM и откройте мир технологий
              </p>
              <a
                href={TELEGRAM}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-6 inline-block rounded-xl bg-brand-gradient px-8 py-3.5 text-sm font-semibold text-white shadow-lg transition-opacity hover:opacity-95"
              >
                Записаться на курс
              </a>
            </div>
          </Reveal>
        </section>

        {/* Футер */}
        <footer className="border-t border-white/10">
          <div className="mx-auto flex max-w-6xl flex-col gap-6 px-6 py-10 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <div className="text-lg font-black">
                TEZZ <span className="text-gradient">STEM</span>
              </div>
              <p className="text-sm text-slate-400">Образовательный центр будущего</p>
            </div>
            <div className="text-sm text-slate-400">
              <a
                href={TELEGRAM}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 font-medium text-brand-300 hover:text-brand-200"
              >
                <Send className="h-4 w-4" />
                Telegram: @isbakks
              </a>
              <p className="mt-1">email: ikaoss222@gmail.com</p>
            </div>
          </div>
          <div className="border-t border-white/5 py-4 text-center text-xs text-slate-500">
            © {new Date().getFullYear()} TEZZ STEM. Все права защищены.
          </div>
        </footer>
      </div>
    </div>
  );
}
