
import { ReportTask } from '@/types/reports';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ReportsApiService {
  private async fetchData<T>(endpoint: string, options?: RequestInit): Promise<T> {
    try {
      const response = await fetch(`${API_BASE_URL}/reports${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`Error fetching ${endpoint}:`, error);
      throw error;
    }
  }

  async getReportTasks(): Promise<ReportTask[]> {
    return this.fetchData<ReportTask[]>('/tasks');
  }
}

export const reportsApi = new ReportsApiService();
