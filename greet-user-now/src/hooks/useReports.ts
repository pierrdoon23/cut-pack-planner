
import { useQuery } from '@tanstack/react-query';
import { reportsApi } from '@/services/reportsApi';
import { ReportTask, GanttTask } from '@/types/reports';

export const useReportTasks = () => {
  return useQuery({
    queryKey: ['reports', 'tasks'],
    queryFn: () => reportsApi.getReportTasks(),
  });
};

export const useGanttData = () => {
  const { data: reportTasks, ...rest } = useReportTasks();

  const ganttTasks: GanttTask[] = reportTasks?.map(task => ({
    id: task.id,
    name: task.name,
    start: task.start_time ? new Date(task.start_time) : new Date(),
    end: task.end_time ? new Date(task.end_time) : new Date(),
    progress: task.end_time ? 100 : 50, // Если есть end_time, считаем завершенной
  })) || [];

  return {
    data: ganttTasks,
    ...rest
  };
};
