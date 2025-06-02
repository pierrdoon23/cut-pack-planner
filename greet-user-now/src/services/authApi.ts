
import { LoginRequest, LoginResponse } from '@/types/users';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class AuthApiService {
  private async fetchData<T>(endpoint: string, options?: RequestInit): Promise<T> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error(`HTTP error! status: ${response.status}, body: ${errorText}`);
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`Error fetching ${endpoint}:`, error);
      throw error;
    }
  }

  async login(data: LoginRequest): Promise<LoginResponse> {
    console.log('Отправляем данные для авторизации:', data);
    return this.fetchData('/users/login', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async ping(): Promise<{ status: string; message: string }> {
    return this.fetchData('/users/ping');
  }
}

export const authApi = new AuthApiService();
