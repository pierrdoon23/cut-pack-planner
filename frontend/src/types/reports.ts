
export interface ReportTask {
  id: number;
  name: string;
  start_time: string | null;
  end_time: string | null;
  material_used?: number;
  waste?: number;
  value?: number;
  base_material?: {
    name: string;
    length: number;
    width: number;
    thickness: number;
    package_type: string;
  };
  target_packaging?: {
    name: string;
    purpose: string;
    length: number;
    width: number;
    package_type: string;
    seam_type: string;
    is_two_streams: boolean;
  };
  machine?: {
    name: string;
    cutting_speed: number;
    machine_width: number;
  };
  user?: {
    full_name: string;
    role: string;
  };
}

export interface GanttTask {
  id: number;
  name: string;
  start: Date;
  end: Date;
  progress?: number;
  dependencies?: number[];
}
