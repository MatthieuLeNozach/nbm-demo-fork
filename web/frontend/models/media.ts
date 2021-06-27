import { MediaLabel } from "@/models/medialabel";

interface Media {
  id: number;
  origin_id?: number;
  type: string;
  file_url?: string;
  file_source?: string;
  meta?: string;
  derivates?: Array<Media>;
  created_at: Date;
  created_by: number;
  updated_at?: Date;
  updated_by?: number;
  device_id: number;
  site_id: number;
  begin_date: Date;
  duration: string;
  medialabels_count?: number;
}

interface InvalidLine {
  line: number;
  content: string;
  detail?: string;
}

interface MediaUploadResponse {
  invalid_lines: Array<InvalidLine>;
  media: Media;
  medialabels: Array<MediaLabel>;
}

export type { Media, MediaUploadResponse };
