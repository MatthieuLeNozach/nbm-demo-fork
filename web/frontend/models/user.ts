interface User {
  id: number;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  full_name?: string;
}

export type { User };
