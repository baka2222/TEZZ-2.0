import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import api from '../api/axios';

export default function ProtectedRoute({ children }) {
  const [checking, setChecking] = useState(true);
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    let mounted = true;

    const validate = async () => {
      // если нет токена в localStorage — сразу нет доступа
      const token = typeof window !== 'undefined' ? localStorage.getItem('access') : null;
      if (!token) {
        if (mounted) {
          setAuthorized(false);
          setChecking(false);
        }
        return;
      }

      try {
        // делаем легкий запрос валидации — заменяй на реальный endpoint, если нужен POST
        // важно: endpoint должен вернуть 200, если токен валиден
        await api.get('/profile/'); // <-- поменяй, если у тебя другой путь
        if (mounted) setAuthorized(true);
      } catch (err) {
        // при 401/ошибке валидации — interceptor в axios уже очистит токен/редиректит,
        // но на всякий случай обновим состояние
        if (mounted) setAuthorized(false);
      } finally {
        if (mounted) setChecking(false);
      }
    };

    validate();

    return () => { mounted = false; };
  }, []);

  if (checking) {
    return (
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', padding: 40}}>
        <div className="loading-spinner" />
        <p>Проверка авторизации...</p>
      </div>
    );
  }

  if (!authorized) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
