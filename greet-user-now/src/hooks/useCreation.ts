
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { creationApi } from '@/services/creationApi';
import { BaseMaterialCreate, TargetPackagingCreate, MachineCreate, UserCreate, TaskCreate, TaskInfoCreate } from '@/types/creation';

// Base Materials
export const useBaseMaterials = () => {
  return useQuery({
    queryKey: ['creation', 'baseMaterials'],
    queryFn: () => creationApi.getBaseMaterials(),
  });
};

export const useCreateBaseMaterial = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (material: BaseMaterialCreate) => creationApi.createBaseMaterial(material),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['creation', 'baseMaterials'] });
    },
  });
};

export const useDeleteBaseMaterial = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (materialId: number) => creationApi.deleteBaseMaterial(materialId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['creation', 'baseMaterials'] });
    },
  });
};

// Target Packaging
export const useTargetPackaging = () => {
  return useQuery({
    queryKey: ['creation', 'targetPackaging'],
    queryFn: () => creationApi.getTargetPackaging(),
  });
};

export const useCreateTargetPackaging = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (packaging: TargetPackagingCreate) => creationApi.createTargetPackaging(packaging),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['creation', 'targetPackaging'] });
    },
  });
};

export const useDeleteTargetPackaging = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (packageId: number) => creationApi.deleteTargetPackaging(packageId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['creation', 'targetPackaging'] });
    },
  });
};

// Machines
export const useMachines = () => {
  return useQuery({
    queryKey: ['creation', 'machines'],
    queryFn: () => creationApi.getMachines(),
  });
};

export const useCreateMachine = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (machine: MachineCreate) => creationApi.createMachine(machine),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['creation', 'machines'] });
    },
  });
};

export const useDeleteMachine = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (machineId: number) => creationApi.deleteMachine(machineId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['creation', 'machines'] });
    },
  });
};

// Users
export const useCreateUser = () => {
  return useMutation({
    mutationFn: (user: UserCreate) => creationApi.createUser(user),
  });
};

// Tasks
export const useCreationTasks = () => {
  return useQuery({
    queryKey: ['creation', 'tasks'],
    queryFn: () => creationApi.getTasks(),
  });
};

export const useCreateCreationTask = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (task: TaskCreate) => creationApi.createTask(task),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['creation', 'tasks'] });
    },
  });
};

// Task Info
export const useCreateTaskInfo = () => {
  return useMutation({
    mutationFn: (info: TaskInfoCreate) => creationApi.createTaskInfo(info),
  });
};
