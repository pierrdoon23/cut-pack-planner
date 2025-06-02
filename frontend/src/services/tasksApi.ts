import { Task, TaskInfo, TaskCreate, CreateTaskResponse, BaseMaterial, TargetPackaging, Machine, TaskStatus } from '@/types/tasks';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class TasksApiService {
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

  async getTasks(): Promise<Task[]> {
    return this.fetchData<Task[]>('/tasks/');
  }

  async getTaskInfo(): Promise<TaskInfo[]> {
    return this.fetchData<TaskInfo[]>('/tasks/info');
  }

  async getCuttingMaps(): Promise<Task[]> {
    return this.fetchData<Task[]>('/tasks/cutting-maps');
  }

  async getBaseMaterials(): Promise<BaseMaterial[]> {
    return this.fetchData<BaseMaterial[]>('/tasks/base-materials');
  }

  async getTargetPackaging(): Promise<TargetPackaging[]> {
    return this.fetchData<TargetPackaging[]>('/tasks/target-packaging');
  }

  async getMachines(): Promise<Machine[]> {
    return this.fetchData<Machine[]>('/tasks/machines');
  }

  async createTask(task: TaskCreate): Promise<CreateTaskResponse> {
    console.log('Отправляем данные для создания задачи:', task);
    return this.fetchData<CreateTaskResponse>('/tasks/', {
      method: 'POST',
      body: JSON.stringify(task),
    });
  }

  async updateTaskStatus(taskId: number, status: TaskStatus): Promise<Task> {
    console.log(`Обновляем статус задачи ${taskId} на ${status}`);
    
    return this.fetchData<Task>(`/tasks/${taskId}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status }),
    });
  }

  async deleteTask(taskId: number): Promise<{ message: string }> {
    return this.fetchData<{ message: string }>(`/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async calculateTask(taskId: number, requiredPieces: number): Promise<unknown> {
    console.log(`Расчет для задачи ${taskId} с количеством ${requiredPieces}`);
    return this.fetchData(`/tasks/${taskId}/calculate`, {
      method: 'POST',
      body: JSON.stringify({ required_pieces: requiredPieces }),
    });
  }
}

export const tasksApi = new TasksApiService();
