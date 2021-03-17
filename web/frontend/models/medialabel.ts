interface MediaLabel {
  id: number;
  media_id: number;
  begin_time: number;
  end_time: number;
  low_freq?: number;
  high_freq?: number;
  label_id: number;
  label_confidence: number;
  created_at: Date;
  created_by: number;
  updated_at?: Date;
  updated_by?: number;
}

export type { MediaLabel };
