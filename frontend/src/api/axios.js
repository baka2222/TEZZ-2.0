import axios from 'axios';

const instance = axios.create({
  baseURL: 'https://tezz.kg/api/',
  headers: { 'Content-Type': 'application/json' },
});

// --- helper to set/clear Authorization header ---
export function setAuthToken(token) {
  if (token) {
    instance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    localStorage.setItem('access', token);
  } else {
    delete instance.defaults.headers.common['Authorization'];
    localStorage.removeItem('access');
  }
}

export function clearAuthToken() {
  delete instance.defaults.headers.common['Authorization'];
  localStorage.removeItem('access');
}

// attach token from localStorage on init (keeps backward compatibility)
const token = typeof window !== 'undefined' ? localStorage.getItem('access') : null;
if (token) {
  instance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

// --- response interceptor: если 401 — очистить токен и редирект на логин ---
let isRedirecting = false;
instance.interceptors.response.use(
  (res) => res,
  (error) => {
    const status = error?.response?.status;
    if (status === 401) {
      // предотвращаем многократные редиректы
      if (!isRedirecting) {
        isRedirecting = true;
        clearAuthToken();
        // короткая задержка, чтобы текущие промисы успели откатиться
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default instance;
