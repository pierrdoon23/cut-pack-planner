
import { 
  BaseMaterial, 
  BaseMaterialCreate, 
  TargetPackaging, 
  TargetPackagingCreate, 
  Machine, 
  MachineCreate, 
  User, 
  UserCreate, 
  Task, 
  TaskCreate, 
  TaskInfoCreate 
} from '@/types/creation';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class CreationApiService {
  private async fetchData<T>(endpoint: string, options?: RequestInit): Promise<T> {
    try {
      const response = await fetch(`${API_BASE_URL}/creation${endpoint}`, {
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

  async getBaseMaterials(): Promise<BaseMaterial[]> {
    return this.fetchData<BaseMaterial[]>('/base_materials');
  }

  async createBaseMaterial(material: BaseMaterialCreate): Promise<BaseMaterial> {
    console.log('Создаем базовый материал:', material);
    return this.fetchData<BaseMaterial>('/base_materials', {
      method: 'POST',
      body: JSON.stringify(material),
    });
  }

  async deleteBaseMaterial(materialId: number): Promise<{ message: string }> {
    return this.fetchData<{ message: string }>(`/base_materials/${materialId}`, {
      method: 'DELETE',
    });
  }

  async getTargetPackaging(): Promise<TargetPackaging[]> {
    return this.fetchData<TargetPackaging[]>('/target_packaging');
  }

  async createTargetPackaging(packaging: TargetPackagingCreate): Promise<TargetPackaging> {
    console.log('Создаем целевую упаковку:', packaging);
    return this.fetchData<TargetPackaging>('/target_packaging', {
      method: 'POST',
      body: JSON.stringify(packaging),
    });
  }

  async deleteTargetPackaging(packageId: number): Promise<{ message: string }> {
    return this.fetchData<{ message: string }>(`/target_packaging/${packageId}`, {
      method: 'DELETE',
    });
  }

  async getMachines(): Promise<Machine[]> {
    return this.fetchData<Machine[]>('/machines');
  }

  async createMachine(machine: MachineCreate): Promise<Machine> {
    console.log('Создаем станок:', machine);
    return this.fetchData<Machine>('/machines', {
      method: 'POST',
      body: JSON.stringify(machine),
    });
  }

  async deleteMachine(machineId: number): Promise<{ message: string }> {
    return this.fetchData<{ message: string }>(`/machines/${machineId}`, {
      method: 'DELETE',
    });
  }

  async createUser(user: UserCreate): Promise<User> {
    console.log('Создаем пользователя:', user);
    return this.fetchData<User>('/users', {
      method: 'POST',
      body: JSON.stringify(user),
    });
  }

  async getTasks(): Promise<Task[]> {
    return this.fetchData<Task[]>('/tasks');
  }

  async createTask(task: TaskCreate): Promise<Task> {
    console.log('Создаем задачу:', task);
    return this.fetchData<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(task),
    });
  }

  async createTaskInfo(info: TaskInfoCreate): Promise<unknown> {
    console.log('Создаем информацию о задаче:', info);
    return this.fetchData('/task_info', {
      method: 'POST',
      body: JSON.stringify(info),
    });
  }
}

export const creationApi = new CreationApiService();
