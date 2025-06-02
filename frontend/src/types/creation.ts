export type PackagingType = 'vacuum' | 'flow_pack' | 'shrink';
export type SeamType = 'double_seam' | 'single_seam' | 'ultrasonic';

export interface BaseMaterial {
  id: number;
  name: string;
  length: number;
  width: number;
  thickness: number;
  package_type: PackagingType;
}

export interface BaseMaterialCreate {
  name: string;
  length: number;
  width: number;
  thickness: number;
  package_type: PackagingType;
}

export interface TargetPackaging {
  id: number;
  name: string;
  purpose: string;
  length: number;
  width: number;
  package_type: PackagingType;
  seam_type: SeamType;
  is_two_streams: boolean;
}

export interface TargetPackagingCreate {
  name: string;
  purpose: string;
  length: number;
  width: number;
  package_type: PackagingType;
  seam_type: SeamType;
  is_two_streams: boolean;
}

export interface Machine {
  id: number;
  name: string;
  cutting_speed: number;
  machine_width: number;
}

export interface MachineCreate {
  name: string;
  cutting_speed: number;
  machine_width: number;
}

export interface User {
  id: number;
  full_name: string;
  role: string;
}

export interface UserCreate {
  full_name: string;
  password: string;
  role: string;
}

export interface Task {
  id: number;
  base_material_id: number;
  target_packaging_id: number;
  machine_id: number;
  user_id: number;
  status: string;
  start_time: string;
}

export interface TaskCreate {
  base_material_id: number;
  target_packaging_id: number;
  machine_id: number;
  user_id: number;
  status?: string;
  start_time?: string;
}

export interface TaskInfoCreate {
  task_id: number;
  status: string;
  material_used: number;
  waste: number;
}
