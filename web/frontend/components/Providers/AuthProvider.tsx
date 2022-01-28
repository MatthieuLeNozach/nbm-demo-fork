import React, {
  createContext,
  useContext,
  useEffect,
  ReactElement,
  useState,
} from "react";
import { parseCookies, setCookie, destroyCookie } from "nookies";
import { useRouter } from "next/router";
import axios from "axios";
import { useTranslation } from "react-i18next";
import {
  AuthProviderData,
  BasicResponse,
  LoginPayload,
  RegistrationPayload,
} from "@/models/auth";
import { User } from "@/models/user";

const AuthContext = createContext({} as AuthProviderData);

interface Props {
  children: React.ReactElement;
}

function AuthProvider({ children }: Props): ReactElement {
  const cookies = parseCookies();
  const { accessToken } = cookies;
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();
  const { t } = useTranslation();

  const anonymousLoginRoutes = [
    "/",
    "/login",
    "/register",
    "/about",
    "/contact",
    "/welcome",
    "/reset-password",
    "/statistics/species"
  ];

  const callMe = async (token) => {
    try {
      const { data, status } = await axios.get(
        `${process.env.API_URL}/users/me`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      if (status === 200) {
        setUser(data);
        return true;
      }
      return false;
    } catch (error) {
      destroyCookie(null, "accessToken");
      setUser(null);
      return false;
    }
  };

  useEffect(() => {
    if (!accessToken && !anonymousLoginRoutes.includes(router.route)) {
      destroyCookie(null, "accessToken");
      setUser(null);
      router.push("/signin");
    } else if (accessToken && !user) {
      callMe(accessToken);
    }
  }, [accessToken, router.route]);

  const login = async ({
    username,
    password,
  }: LoginPayload): Promise<BasicResponse> => {
    const loginResponse = {
      success: false,
      message: t("errorOnLogin"),
    } as BasicResponse;
    try {
      const payload = new URLSearchParams();
      payload.append("username", username);
      payload.append("password", password);
      const config = {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      };
      const { data, status } = await axios.post(
        `${process.env.API_URL}/login/access-token`,
        payload,
        config
      );
      if (status === 200) {
        const { access_token } = data;
        setCookie(null, "accessToken", access_token, {
          path: "/",
          maxAge: 3600,
          sameSite: true,
        });
        const logged = await callMe(access_token);
        if (logged) {
          loginResponse.success = true;
          loginResponse.message = t("successfulLogin");
        }
      }
    } catch (error) {
      const { response } = error;
      loginResponse.message += Array.isArray(response?.data?.detail)
        ? t(response?.data?.detail[0].type.replace("value_error.", "invalid_"))
        : response?.data?.detail || response.status;
    }
    return loginResponse;
  };

  const register = async (
    payload: RegistrationPayload
  ): Promise<BasicResponse> => {
    const registrationResponse = {
      success: false,
      message: t("errorOnRegistration"),
    } as BasicResponse;
    try {
      const { data, status } = await axios.post(
        `${process.env.API_URL}/register`,
        payload
      );
      if (status === 200) {
        const { access_token, ...userData } = data;
        setCookie(null, "accessToken", access_token, {
          path: "/",
          maxAge: 3600,
          sameSite: true,
        });
        setUser(userData);
        registrationResponse.success = true;
        registrationResponse.message = t("youAreNowRegistered");
      }
    } catch (error) {
      const { response } = error;

      registrationResponse.message += Array.isArray(response?.data?.detail)
        ? t(response?.data?.detail[0].type.replace("value_error.", "invalid_"))
        : response?.data?.detail || response.status;
    }
    return registrationResponse;
  };

  const logout = () => {
    destroyCookie(null, "accessToken");
    setUser(null);
    router.push("/");
  };
  return (
    <AuthContext.Provider
      value={{ user, accessToken, login, register, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}
const useAuth = (): AuthProviderData => useContext(AuthContext);
export { AuthProvider, useAuth };
