
import { useQuery } from '@tanstack/react-query';
import { mainPageApi } from '@/services/mainPageApi';

export const useMainPageData = () => {
  return useQuery({
    queryKey: ['mainPageData'],
    queryFn: () => mainPageApi.getAllMainPageData(),
    refetchInterval: 30000, // Обновляем каждые 30 секунд
    staleTime: 10000, // Данные считаются актуальными 10 секунд
  });
};

export const useRollsCount = () => {
  return useQuery({
    queryKey: ['rollsCount'],
    queryFn: () => mainPageApi.getRollsCount(),
    refetchInterval: 30000,
  });
};

export const useCuttingMapsCount = () => {
  return useQuery({
    queryKey: ['cuttingMapsCount'],
    queryFn: () => mainPageApi.getCuttingMapsCount(),
    refetchInterval: 30000,
  });
};

export const usePackagesCount = () => {
  return useQuery({
    queryKey: ['packagesCount'],
    queryFn: () => mainPageApi.getPackagesCount(),
    refetchInterval: 30000,
  });
};

export const useWeeklyChart = () => {
  return useQuery({
    queryKey: ['weeklyChart'],
    queryFn: () => mainPageApi.getBarChartData(),
    refetchInterval: 60000, // Обновляем каждую минуту
  });
};

export const useCuttingTypes = () => {
  return useQuery({
    queryKey: ['cuttingTypes'],
    queryFn: () => mainPageApi.getCuttingDonutData(),
    refetchInterval: 60000,
  });
};

export const useMaterialUsage = () => {
  return useQuery({
    queryKey: ['materialUsage'],
    queryFn: () => mainPageApi.getUsageDonutData(),
    refetchInterval: 60000,
  });
};
