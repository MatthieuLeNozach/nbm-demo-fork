interface Site {
  id: number;
  name: string;
  longitude: number;
  latitude: number;
  is_private: boolean;
  locality_precision: number;
  created_at: Date;
  created_by: number;
  updated_at?: Date;
  updated_by?: number;
}

interface Position {
  latitude: number;
  longitude: number;
}

export type { Site, Position };
