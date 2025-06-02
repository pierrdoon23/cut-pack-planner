import { User, UserCreate, UserUpdate, LoginRequest, LoginResponse } from '@/types/users';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class UsersApiService {
  private async fetchData<T>(endpoint: string, options?: RequestInit): Promise<T> {
    try {
      const response = await fetch(`${API_BASE_URL}/users${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Произошла ошибка' }));
        throw new Error(error.detail || 'Произошла ошибка');
      }
      
      if (response.status === 204) {
        return {} as T;
      }
      
      return await response.json();
    } catch (error) {
      console.error(`Error fetching ${endpoint}:`, error);
      throw error;
    }
  }

  async ping(): Promise<{ status: string; message: string }> {
    return this.fetchData('/ping');
  }

  async login(data: LoginRequest): Promise<LoginResponse> {
    console.log('Отправляем данные для авторизации через users API:', data);
    return this.fetchData('/login', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getUsers(): Promise<User[]> {
    return this.fetchData('');
  }

  async getUser(userId: number): Promise<User> {
    return this.fetchData(`/${userId}`);
  }

  async createUser(user: UserCreate): Promise<User> {
    console.log('Создаем пользователя через users API:', user);
    return this.fetchData('', {
      method: 'POST',
      body: JSON.stringify(user),
    });
  }

  async updateUser(userId: number, user: UserUpdate): Promise<User> {
    return this.fetchData(`/${userId}`, {
      method: 'PATCH',
      body: JSON.stringify(user),
    });
  }

  async deleteUser(userId: number): Promise<void> {
    await this.fetchData(`/${userId}`, {
      method: 'DELETE',
    });
  }
}

export const usersApi = new UsersApiService();
