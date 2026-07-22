import type { Metadata } from "next";
import LoginView from "@/components/views/LoginView";

export const metadata: Metadata = {
  title: "Вход",
  description: "Войдите в личный кабинет TEZZ.",
};

export default function LoginPage() {
  return <LoginView />;
}
