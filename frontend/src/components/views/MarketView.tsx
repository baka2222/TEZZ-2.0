import Image from "next/image";
import {
  BadgeCheck,
  Bike,
  Bot,
  Car,
  HandCoins,
  Home,
  Megaphone,
  Rocket,
  ShoppingCart,
  Smartphone,
  Sparkles,
  Truck,
  UtensilsCrossed,
  Wrench,
  type LucideIcon,
} from "lucide-react";
import Reveal from "@/components/Reveal";
import HeroCanvas from "@/components/HeroCanvas";

const BOT = "https://t.me/tez4917_bot";

const fadeUp = (delay: number) => ({
  opacity: 0,
  animation: "tm-fade-up .9s cubic-bezier(.16,1,.3,1) both",
  animationDelay: `${delay}s`,
});

const CATEGORIES: { icon: LucideIcon; label: string }[] = [
  { icon: UtensilsCrossed, label: "Еда" },
  { icon: Wrench, label: "Услуги" },
  { icon: Smartphone, label: "Техника" },
  { icon: Home, label: "Дом и быт" },
  { icon: Sparkles, label: "Красота" },
  { icon: Bike, label: "Спорт" },
  { icon: Car, label: "Авто" },
  { icon: BadgeCheck, label: "Одежда" },
];

const STEPS = [
  { n: "01", icon: Megaphone, title: "Смотри витрину", text: "Магазины публикуют товары и услуги в каталоге бота и тематических каналах." },
  { n: "02", icon: Bot, title: "Переходи в бот", text: "Жмёшь «Связаться» под товаром — открывается диалог с продавцом в @tez4917_bot." },
  { n: "03", icon: ShoppingCart, title: "Оформляй сделку", text: "Оплата, доставка курьером или запись в мастерскую — бот проведёт до конца." },
];

function Shimmer() {
  return (
    <span
      className="pointer-events-none absolute left-0 top-0 h-full w-2/5"
      style={{
        background: "linear-gradient(90deg,transparent,rgba(255,255,255,0.75),transparent)",
        animation: "tm-shimmer 3.6s ease-in-out infinite",
      }}
    />
  );
}

export default function MarketView() {
  return (
    <div className="min-h-screen bg-[#fbf6e6] font-sans text-[#3d2f24]">
      {/* Хедер */}
      <header
        className="sticky top-0 z-[60] border-b border-white/10 backdrop-blur-[14px]"
        style={{ background: "rgba(27,58,33,0.78)" }}
      >
        <div className="mx-auto flex max-w-[1200px] items-center justify-between gap-4 px-7 py-3.5">
          <div className="flex items-center gap-3">
            <Image src="/tezz_logo.png" alt="TEZZ" width={42} height={42} className="object-contain" priority />
            <div className="leading-tight">
              <div className="text-[17px] font-extrabold tracking-wide text-[#fbf6e6]">TEZZ MARKET</div>
              <div className="text-[11px] text-[#fbf6e6]/60">Маркет в Telegram</div>
            </div>
          </div>
          <nav className="hidden items-center gap-6 md:flex">
            <a href="#how" className="text-sm font-semibold text-[#fbf6e6]/85 hover:text-[#fbf6e6]">Как работает</a>
            <a href="#why" className="text-sm font-semibold text-[#fbf6e6]/85 hover:text-[#fbf6e6]">Преимущества</a>
            <a href={BOT} target="_blank" rel="noopener noreferrer" className="text-sm font-semibold text-[#fbf6e6]/85 hover:text-[#fbf6e6]">Каталог</a>
          </nav>
          <a
            href={BOT}
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-[10px] bg-[#fbf6e6] px-[18px] py-2.5 text-sm font-bold text-[#1b3a21]"
          >
            Открыть бот
          </a>
        </div>
      </header>

      {/* Герой */}
      <section
        className="relative overflow-hidden text-[#fbf6e6]"
        style={{
          background:
            "radial-gradient(1100px 560px at 80% 18%, rgba(127,185,138,0.28), transparent 60%), linear-gradient(160deg,#274f2d 0%,#16301c 100%)",
        }}
      >
        <div
          className="absolute -top-[140px] -right-[70px] h-[440px] w-[440px] rounded-full blur-[100px]"
          style={{ background: "rgba(127,185,138,0.28)", animation: "tm-float 17s ease-in-out infinite" }}
        />
        <div
          className="absolute -bottom-[140px] -left-[90px] h-[360px] w-[360px] rounded-full blur-[100px]"
          style={{ background: "rgba(47,107,58,0.4)", animation: "tm-float2 21s ease-in-out infinite" }}
        />

        <div className="relative mx-auto grid max-w-[1200px] items-center gap-11 px-7 pb-[90px] pt-[72px] lg:grid-cols-[1.02fr_0.98fr]">
          <div className="order-2 lg:order-1">
            <div
              className="mb-6 inline-flex items-center gap-2.5 rounded-full border border-[#fbf6e6]/20 bg-[#fbf6e6]/10 px-[15px] py-[7px] text-[13px] font-semibold"
              style={fadeUp(0)}
            >
              <span
                className="h-2 w-2 rounded-full bg-[#7fb98a]"
                style={{ animation: "tm-pulse 2s infinite" }}
              />
              2000+ покупателей уже здесь
            </div>
            <h1
              className="m-0 mb-5 font-black leading-[1.0] tracking-[-1.5px]"
              style={{ fontSize: "clamp(38px,5.6vw,66px)", ...fadeUp(0.08) }}
            >
              Весь маркет —<br />
              <span className="text-[#7fb98a]">в одном Telegram-боте</span>
            </h1>
            <p
              className="m-0 mb-8 max-w-[520px] leading-[1.65] text-[#fbf6e6]/80"
              style={{ fontSize: "clamp(15px,1.6vw,18px)", ...fadeUp(0.16) }}
            >
              Товары, услуги и магазины со всего Кыргызстана. Смотри витрину,
              договаривайся с продавцом и оформляй доставку — без лишних приложений
              и комиссий.
            </p>
            <div className="mb-11 flex flex-wrap gap-3.5" style={fadeUp(0.24)}>
              <a
                href={BOT}
                target="_blank"
                rel="noopener noreferrer"
                className="relative inline-flex items-center gap-2 overflow-hidden rounded-[14px] bg-[#fbf6e6] px-7 py-4 text-base font-extrabold text-[#1b3a21]"
                style={{ boxShadow: "0 14px 34px rgba(0,0,0,0.28)" }}
              >
                <Rocket className="h-5 w-5" />
                Начать покупать
                <Shimmer />
              </a>
              <a
                href={BOT}
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-[14px] border border-[#fbf6e6]/30 bg-[#fbf6e6]/10 px-7 py-4 text-base font-bold text-[#fbf6e6]"
              >
                Смотреть каталог
              </a>
            </div>
            <div className="flex flex-wrap gap-9" style={fadeUp(0.32)}>
              {[
                { v: "0%", l: "комиссии" },
                { v: "1 клик", l: "до сделки" },
              ].map((s) => (
                <div key={s.l}>
                  <div className="text-[27px] font-black">{s.v}</div>
                  <div className="text-[13px] text-[#fbf6e6]/70">{s.l}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="order-1 lg:order-2">
            <HeroCanvas />
          </div>
        </div>

        {/* Бегущая строка категорий */}
        <div
          className="relative overflow-hidden border-t border-[#fbf6e6]/10 py-4"
          style={{ background: "rgba(0,0,0,0.12)" }}
        >
          <div
            className="flex w-max gap-3.5"
            style={{ animation: "tm-marquee 26s linear infinite" }}
          >
            {[...CATEGORIES, ...CATEGORIES].map((c, i) => (
              <span
                key={i}
                className="inline-flex flex-none items-center gap-2 whitespace-nowrap rounded-full border border-[#fbf6e6]/15 bg-[#fbf6e6]/[0.09] px-[18px] py-2 text-sm font-semibold text-[#fbf6e6]"
              >
                <c.icon className="h-4 w-4 text-[#7fb98a]" />
                {c.label}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Как это работает */}
      <section id="how" className="mx-auto max-w-[1200px] px-7 py-[90px]">
        <Reveal className="max-w-[640px]">
          <div className="mb-3 text-[13px] font-extrabold uppercase tracking-[2px] text-[#2f6b3a]">
            Как это работает
          </div>
          <h2
            className="m-0 mb-3 font-black leading-[1.05] tracking-[-0.8px]"
            style={{ fontSize: "clamp(28px,3.6vw,42px)" }}
          >
            От витрины до покупки — три шага
          </h2>
          <p className="m-0 mb-12 text-[17px] leading-[1.6] text-[#6b6b6b]">
            Всё происходит внутри Telegram. Никаких регистраций и установок.
          </p>
        </Reveal>
        <div className="grid gap-[22px] md:grid-cols-3">
          {STEPS.map((s, i) => (
            <Reveal
              key={s.n}
              delay={i * 120}
              className="rounded-[22px] bg-white p-8"
            >
              <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-[#2f6b3a]/10 text-[#2f6b3a]">
                <s.icon className="h-6 w-6" />
              </div>
              <h3 className="m-0 mb-2 text-xl font-bold">{s.title}</h3>
              <p className="m-0 text-sm leading-[1.65] text-[#6b6b6b]">{s.text}</p>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Преимущества */}
      <section id="why" className="text-[#fbf6e6]" style={{ background: "linear-gradient(160deg,#274f2d,#16301c)" }}>
        <div className="mx-auto max-w-[1200px] px-7 py-[90px]">
          <Reveal className="mb-12 max-w-[640px]">
            <div className="mb-3 text-[13px] font-extrabold uppercase tracking-[2px] text-[#7fb98a]">
              Преимущества
            </div>
            <h2
              className="m-0 font-black leading-[1.05] tracking-[-0.8px]"
              style={{ fontSize: "clamp(28px,3.6vw,42px)" }}
            >
              Почему покупают через TezzMarket
            </h2>
          </Reveal>

          <div className="grid gap-[18px] md:grid-cols-[1.4fr_1fr]">
            <Reveal className="flex min-h-[280px] flex-col justify-between rounded-3xl border border-[#fbf6e6]/10 bg-[#fbf6e6]/[0.06] p-9 md:row-span-2">
              <HandCoins className="h-10 w-10 text-[#7fb98a]" />
              <div>
                <h3 className="m-0 mb-2.5 text-[26px] font-black">Полностью бесплатно</h3>
                <p className="m-0 text-[15px] leading-[1.65] text-[#fbf6e6]/80">
                  Никаких комиссий за покупку или размещение объявлений. Платно —
                  только ускоренный повтор объявления, и то по желанию.
                </p>
              </div>
            </Reveal>
            <Reveal delay={120} className="rounded-3xl border border-[#fbf6e6]/10 bg-[#fbf6e6]/[0.06] p-7">
              <Truck className="mb-3.5 h-8 w-8 text-[#7fb98a]" />
              <h3 className="m-0 mb-1.5 text-[19px] font-bold">Доставка через бота</h3>
              <p className="m-0 text-sm leading-[1.6] text-[#fbf6e6]/70">
                Курьер и авторасчёт цены по расстоянию — всё в Telegram.
              </p>
            </Reveal>
            <Reveal delay={200} className="rounded-3xl border border-[#fbf6e6]/10 bg-[#fbf6e6]/[0.06] p-7">
              <BadgeCheck className="mb-3.5 h-8 w-8 text-[#7fb98a]" />
              <h3 className="m-0 mb-1.5 text-[19px] font-bold">Проверенные продавцы</h3>
              <p className="m-0 text-sm leading-[1.6] text-[#fbf6e6]/70">
                Модерация исключает мошенников — только реальные объявления.
              </p>
            </Reveal>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-[1100px] px-7 py-[100px]">
        <Reveal
          className="relative overflow-hidden rounded-[30px] bg-[linear-gradient(120deg,#2f6b3a,#1b3a21)] p-[clamp(40px,6vw,72px)] text-center text-[#fbf6e6]"
        >
          <div
            className="absolute -top-[120px] -left-[60px] h-[320px] w-[320px] rounded-full blur-[80px]"
            style={{ background: "rgba(127,185,138,0.3)", animation: "tm-float 15s ease-in-out infinite" }}
          />
          <div
            className="absolute -bottom-[120px] -right-[40px] h-[280px] w-[280px] rounded-full blur-[80px]"
            style={{ background: "rgba(251,246,230,0.14)", animation: "tm-float2 18s ease-in-out infinite" }}
          />
          <div className="relative">
            <h2
              className="m-0 mb-4 font-black leading-[1.05] tracking-[-1px]"
              style={{ fontSize: "clamp(30px,4.4vw,52px)" }}
            >
              Готов покупать умнее?
            </h2>
            <p
              className="mx-auto mb-[34px] max-w-[520px] leading-[1.6] text-[#fbf6e6]/85"
              style={{ fontSize: "clamp(15px,1.7vw,19px)" }}
            >
              Открой бота, выбери товар и оформи сделку за пару минут. Бесплатно.
            </p>
            <a
              href={BOT}
              target="_blank"
              rel="noopener noreferrer"
              className="relative inline-block overflow-hidden rounded-2xl bg-[#fbf6e6] px-10 py-[18px] text-lg font-extrabold text-[#1b3a21]"
              style={{ boxShadow: "0 18px 40px rgba(0,0,0,0.3)" }}
            >
              Перейти в @tez4917_bot
              <Shimmer />
            </a>
          </div>
        </Reveal>
      </section>

      {/* Футер */}
      <footer className="border-t border-[#3d2f24]/10">
        <div className="mx-auto flex max-w-[1200px] flex-wrap items-center justify-between gap-4 px-7 py-7 text-sm text-[#6b6b6b]">
          <div className="flex items-center gap-2.5">
            <Image src="/tezz_logo.png" alt="TEZZ" width={32} height={32} className="object-contain" />
            <span>© 2026 TEZZ MARKET</span>
          </div>
          <div>
            Работает в Telegram ·{" "}
            <a href={BOT} target="_blank" rel="noopener noreferrer" className="font-semibold text-[#2f6b3a]">
              @tez4917_bot
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
