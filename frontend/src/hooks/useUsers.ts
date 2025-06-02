import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { usersApi } from '@/services/usersApi';
import { UserCreate, UserUpdate, LoginRequest } from '@/types/users';
import { useToast } from '@/components/ui/use-toast';

export const useUsers = () => {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => usersApi.getUsers(),
  });
};

export const useUser = (userId: number) => {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => usersApi.getUser(userId),
    enabled: !!userId,
  });
};

export const useCreateUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (user: UserCreate) => usersApi.createUser(user),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};

export const useUpdateUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ userId, user }: { userId: number; user: UserUpdate }) => 
      usersApi.updateUser(userId, user),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};

export const useDeleteUser = () => {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  
  return useMutation({
    mutationFn: (userId: number) => usersApi.deleteUser(userId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      toast({
        title: "Успех",
        description: "Пользователь успешно удален",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Ошибка",
        description: error.message || "Не удалось удалить пользователя",
        variant: "destructive",
      });
    }
  });
};

export const useLogin = () => {
  return useMutation({
    mutationFn: (data: LoginRequest) => usersApi.login(data),
  });
};

export const usePing = () => {
  return useQuery({
    queryKey: ['ping'],
    queryFn: () => usersApi.ping(),
    refetchInterval: 30000,
  });
};
