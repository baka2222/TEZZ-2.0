"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, getToken } from "@/lib/api";
import { PageLoader } from "./ui";

/**
 * Клиентский guard: проверяет токен через /profile/.
 * Нет токена или 401 → редирект на /login (сам api.get дернёт редирект при 401).
 */
export default function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [state, setState] = useState<"checking" | "ok">("checking");

  useEffect(() => {
    let active = true;
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    api
      .get("/profile/")
      .then(() => {
        if (active) setState("ok");
      })
      .catch(() => {
        if (active) router.replace("/login");
      });
    return () => {
      active = false;
    };
  }, [router]);

  if (state === "checking") return <PageLoader label="Проверка авторизации…" />;
  return <>{children}</>;
}
