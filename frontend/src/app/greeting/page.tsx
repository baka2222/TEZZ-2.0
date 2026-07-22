import type { Metadata } from "next";
import GreetingView from "@/components/views/GreetingView";

export const metadata: Metadata = {
  title: "STEM-курсы в Бишкеке — программирование, робототехника, ОРТ",
  description:
    "Онлайн и оффлайн курсы по программированию, робототехнике, физике и математике для детей и подростков.",
  openGraph: {
    title: "TEZZ — STEM-курсы в Бишкеке",
    description:
      "Программирование, робототехника, физика и математика. Практические навыки для будущего.",
    url: "https://tezz.kg/greeting",
    type: "website",
  },
};

export default function GreetingPage() {
  return <GreetingView />;
}
