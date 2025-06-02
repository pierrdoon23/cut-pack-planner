import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { tasksApi } from '@/services/tasksApi';
import { TaskCreate, TaskStatus } from '@/types/tasks';

export const useTasks = () => {
  return useQuery({
    queryKey: ['tasks'],
    queryFn: () => tasksApi.getTasks(),
    refetchInterval: 30000,
  });
};

export const useTaskInfo = () => {
  return useQuery({
    queryKey: ['taskInfo'],
    queryFn: () => tasksApi.getTaskInfo(),
    refetchInterval: 30000,
  });
};

export const useCuttingMaps = () => {
  return useQuery({
    queryKey: ['cuttingMaps'],
    queryFn: () => tasksApi.getCuttingMaps(),
    refetchInterval: 30000,
  });
};

export const useBaseMaterials = () => {
  return useQuery({
    queryKey: ['baseMaterials'],
    queryFn: () => tasksApi.getBaseMaterials(),
  });
};

export const useTargetPackaging = () => {
  return useQuery({
    queryKey: ['targetPackaging'],
    queryFn: () => tasksApi.getTargetPackaging(),
  });
};

export const useMachines = () => {
  return useQuery({
    queryKey: ['machines'],
    queryFn: () => tasksApi.getMachines(),
  });
};

export const useCreateTask = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (task: TaskCreate) => tasksApi.createTask(task),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      queryClient.invalidateQueries({ queryKey: ['taskInfo'] });
      queryClient.invalidateQueries({ queryKey: ['cuttingMaps'] });
    },
  });
};

export const useUpdateTaskStatus = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ taskId, status }: { taskId: number; status: TaskStatus }) => 
      tasksApi.updateTaskStatus(taskId, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      queryClient.invalidateQueries({ queryKey: ['taskInfo'] });
      queryClient.invalidateQueries({ queryKey: ['cuttingMaps'] });
    },
  });
};

export const useDeleteTask = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (taskId: number) => tasksApi.deleteTask(taskId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      queryClient.invalidateQueries({ queryKey: ['taskInfo'] });
      queryClient.invalidateQueries({ queryKey: ['cuttingMaps'] });
    },
  });
};

export const useCalculateTask = () => {
  return useMutation({
    mutationFn: ({ taskId, requiredPieces }: { taskId: number; requiredPieces: number }) => 
      tasksApi.calculateTask(taskId, requiredPieces),
  });
};
