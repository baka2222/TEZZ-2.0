import type { Metadata } from "next";
import MarketView from "@/components/views/MarketView";

export const metadata: Metadata = {
  title: "TEZZ MARKET — покупка и продажа в Telegram",
  description:
    "Объявления из Telegram-каналов, покупка через бота @tez4917_bot. Веломаркет, техника, услуги мастерских. Всё бесплатно.",
  // Раздел маркета — лого tezz (отдельная система от EduTech).
  icons: { icon: "/tezz_logo.png", apple: "/tezz_logo.png" },
  openGraph: {
    title: "TEZZ MARKET — покупка в Telegram",
    description:
      "Покупайте велосипеды, технику и услуги прямо в Telegram. Быстро, бесплатно, надёжно.",
    url: "https://t.me/tez4917_bot",
    type: "website",
  },
};

export default function MarketPage() {
  return <MarketView />;
}
