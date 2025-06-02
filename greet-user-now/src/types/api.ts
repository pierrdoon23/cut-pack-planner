
export interface CountData {
  total: number;
  last_24h: number;
}

export interface WeeklyChartData {
  labels: string[];
  values: number[];
}

export interface CuttingTypeData {
  type: string;
  percent: number;
}

export interface MaterialUsageData {
  used_percent: number;
  wasted_percent: number;
}

export interface MainPageApiResponse {
  rollsCount: CountData;
  cuttingMapsCount: CountData;
  packagesCount: CountData;
  weeklyChart: WeeklyChartData;
  cuttingTypes: CuttingTypeData[];
  materialUsage: MaterialUsageData;
}
