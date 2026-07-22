/**
 * Лёгкий клиент к Django REST API (замена прежнего axios).
 *
 * Авторизация — JWT в localStorage (Bearer). Все запросы идут на /api/*,
 * который в деве проксируется на Django (см. next.config.ts), а в проде
 * обслуживается тем же nginx. При 401 токен очищается и уходим на /login.
 */

const ACCESS_KEY = "access";
const REFRESH_KEY = "refresh";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(ACCESS_KEY);
}

export function setTokens(access: string, refresh?: string) {
  if (typeof window === "undefined") return;
  localStorage.setItem(ACCESS_KEY, access);
  if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
}

export function clearTokens() {
  if (typeof window === "undefined") return;
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
}

export class ApiError extends Error {
  status: number;
  data: unknown;
  constructor(status: number, message: string, data?: unknown) {
    super(message);
    this.status = status;
    this.data = data;
  }
}

let redirecting = false;

type Method = "GET" | "POST" | "PATCH" | "PUT" | "DELETE";

async function request<T>(
  method: Method,
  path: string,
  body?: unknown,
  opts: { auth?: boolean } = {},
): Promise<T> {
  const { auth = true } = opts;
  const isForm = typeof FormData !== "undefined" && body instanceof FormData;

  const headers: Record<string, string> = {};
  if (body !== undefined && !isForm) headers["Content-Type"] = "application/json";
  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`/api${path}`, {
    method,
    headers,
    body: body === undefined ? undefined : isForm ? (body as FormData) : JSON.stringify(body),
  });

  if (res.status === 401) {
    clearTokens();
    if (typeof window !== "undefined" && !redirecting) {
      redirecting = true;
      window.location.href = "/login";
    }
    throw new ApiError(401, "Unauthorized");
  }

  if (!res.ok) {
    let data: unknown = null;
    try {
      data = await res.json();
    } catch {
      /* пустое тело */
    }
    throw new ApiError(res.status, `Request failed: ${res.status}`, data);
  }

  if (res.status === 204) return undefined as T;
  const ct = res.headers.get("content-type") ?? "";
  if (!ct.includes("application/json")) return undefined as T;
  return (await res.json()) as T;
}

export const api = {
  get: <T>(path: string, opts?: { auth?: boolean }) => request<T>("GET", path, undefined, opts),
  post: <T>(path: string, body?: unknown, opts?: { auth?: boolean }) =>
    request<T>("POST", path, body, opts),
  patch: <T>(path: string, body?: unknown, opts?: { auth?: boolean }) =>
    request<T>("PATCH", path, body, opts),
};

/** Вход: POST /api/api/token/ (эндпоинт SimpleJWT примонтирован именно так). */
export async function login(username: string, password: string) {
  const data = await api.post<{ access: string; refresh?: string }>(
    "/api/token/",
    { username, password },
    { auth: false },
  );
  setTokens(data.access, data.refresh);
  return data;
}

export function logout() {
  clearTokens();
  if (typeof window !== "undefined") window.location.href = "/login";
}
