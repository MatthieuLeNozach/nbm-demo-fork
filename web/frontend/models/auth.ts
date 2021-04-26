import { User } from "@/models/user";

interface LoginPayload {
  username: string;
  password: string;
}

interface RegistrationPayload {
  email: string;
  full_name: string;
  password: string;
  password_confirmation: string;
}

interface BasicResponse {
  success: boolean;
  message: string;
}

interface AuthProviderData {
  login(props: LoginPayload): Promise<BasicResponse>;
  logout(): void;
  register(payload: RegistrationPayload): Promise<BasicResponse>;
  user?: User;
  accessToken?: string;
}

export type {
  AuthProviderData,
  BasicResponse,
  RegistrationPayload,
  LoginPayload,
};
