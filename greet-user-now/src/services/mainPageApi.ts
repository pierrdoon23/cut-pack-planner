import { CountData, WeeklyChartData, CuttingTypeData, MaterialUsageData } from '@/types/api';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class MainPageApiService {
  private async fetchData<T>(endpoint: string): Promise<T> {
    try {
      const response = await fetch(`${API_BASE_URL}/mainpage${endpoint}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`Error fetching ${endpoint}:`, error);
      throw error;
    }
  }

  async getRollsCount(): Promise<CountData> {
    return this.fetchData<CountData>('/rolls_count');
  }

  async getCuttingMapsCount(): Promise<CountData> {
    return this.fetchData<CountData>('/cutting_maps_count');
  }

  async getPackagesCount(): Promise<CountData> {
    return this.fetchData<CountData>('/packages_count');
  }

  async getBarChartData(): Promise<WeeklyChartData> {
    return this.fetchData<WeeklyChartData>('/bar_chart');
  }

  async getCuttingDonutData(): Promise<CuttingTypeData[]> {
    return this.fetchData<CuttingTypeData[]>('/donut_cutting');
  }

  async getUsageDonutData(): Promise<MaterialUsageData> {
    return this.fetchData<MaterialUsageData>('/donut_usage');
  }

  async getAllMainPageData() {
    try {
      const [
        rollsCount,
        cuttingMapsCount,
        packagesCount,
        weeklyChart,
        cuttingTypes,
        materialUsage
      ] = await Promise.all([
        this.getRollsCount(),
        this.getCuttingMapsCount(),
        this.getPackagesCount(),
        this.getBarChartData(),
        this.getCuttingDonutData(),
        this.getUsageDonutData()
      ]);

      return {
        rollsCount,
        cuttingMapsCount,
        packagesCount,
        weeklyChart,
        cuttingTypes,
        materialUsage
      };
    } catch (error) {
      console.error('Error fetching main page data:', error);
      throw error;
    }
  }
}

export const mainPageApi = new MainPageApiService();
