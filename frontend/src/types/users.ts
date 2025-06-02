export type UserRole = 'admin' | 'operator';

export interface User {
  id: number;
  full_name: string;
  role: UserRole;
}

export interface UserCreate {
  full_name: string;
  password: string;
  role: UserRole;
}

export interface UserUpdate {
  full_name?: string;
  password?: string;
  role?: UserRole;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  id: number;
  full_name: string;
  role: string;
  token?: string;
}
