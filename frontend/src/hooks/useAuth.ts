
import { useState, useEffect } from 'react';
import { useMutation } from '@tanstack/react-query';
import { authApi } from '@/services/authApi';
import { LoginRequest, LoginResponse } from '@/types/users';

interface AuthState {
  isAuthenticated: boolean;
  user: LoginResponse | null;
}

const COOKIE_NAME = 'auth_data';
const COOKIE_EXPIRY_DAYS = 14;

const setCookie = (name: string, value: string, days: number) => {
  const expires = new Date();
  expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
  document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Strict`;
};

const getCookie = (name: string): string | null => {
  const nameEQ = name + '=';
  const ca = document.cookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
};

const deleteCookie = (name: string) => {
  document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
};

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
  });

  // Проверяем куки при загрузке
  useEffect(() => {
    const savedAuth = getCookie(COOKIE_NAME);
    if (savedAuth) {
      try {
        const userData = JSON.parse(decodeURIComponent(savedAuth));
        setAuthState({
          isAuthenticated: true,
          user: userData,
        });
      } catch (error) {
        console.error('Error parsing saved auth data:', error);
        deleteCookie(COOKIE_NAME);
      }
    }
  }, []);

  const loginMutation = useMutation({
    mutationFn: (data: LoginRequest) => authApi.login(data),
    onSuccess: (userData) => {
      // Сохраняем данные пользователя в куки на 14 дней
      setCookie(COOKIE_NAME, encodeURIComponent(JSON.stringify(userData)), COOKIE_EXPIRY_DAYS);
      
      setAuthState({
        isAuthenticated: true,
        user: userData,
      });
    },
    onError: (error) => {
      console.error('Login failed:', error);
    },
  });

  const logout = () => {
    deleteCookie(COOKIE_NAME);
    setAuthState({
      isAuthenticated: false,
      user: null,
    });
  };

  const login = (username: string, password: string) => {
    return loginMutation.mutate({ username, password });
  };

  return {
    ...authState,
    login,
    logout,
    isLoading: loginMutation.isPending,
    error: loginMutation.error,
  };
};
