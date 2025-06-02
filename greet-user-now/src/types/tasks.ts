export type TaskStatus = 'planned' | 'in_progress' | 'completed' | 'cancelled';

export interface BaseMaterial {
  id: number;
  name: string;
  length: number;
  width: number;
  thickness: number;
  package_type: string;
}

export interface TargetPackaging {
  id: number;
  name: string;
  purpose: string;
  length: number;
  width: number;
  package_type: string;
  seam_type: string;
  is_two_streams: boolean;
}

export interface Machine {
  id: number;
  name: string;
  cutting_speed: number;
  machine_width: number;
}

export interface User {
  id: number;
  full_name: string;
  role: string;
}

export interface TaskInfo {
  task_id: number;
  status: string;
  start_time: string;
  end_time?: string;
  material_used?: number;
  waste?: number;
  value?: number;
  base_material: BaseMaterial;
  target_packaging: TargetPackaging;
  machine: Machine;
  user: User;
}

export interface Task {
  id: number;
  base_material_id: number;
  target_packaging_id: number;
  machine_id: number;
  user_id: number;
  start_time: string;
  status: string;
}

export interface TaskCreate {
  base_material_id: number;
  target_packaging_id: number;
  machine_id: number;
  user_id: number;
  status?: string;
  start_time?: string;
}

export interface CalculationResponse {
  task_info: any;
  material_left: number;
  cutting_time_minutes: number;
  total_target_length: number;
}

export interface CreateTaskResponse {
  task: Task;
  calculation: CalculationResponse;
}
