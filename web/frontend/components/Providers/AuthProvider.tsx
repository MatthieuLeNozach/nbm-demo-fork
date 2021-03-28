import { createContext, useContext, useEffect } from "react";
import Backdrop from "@material-ui/core/Backdrop";
import CircularProgress from "@material-ui/core/CircularProgress";
import { makeStyles } from "@material-ui/core/styles";
import useLocalStorage from "@/hooks/useLocalStorage";
import { useRouter } from "next/router";
import axios from "axios";
import { useTranslation } from "react-i18next";

interface IUser {
  id: number;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  full_name: string;
}

const useStyles = makeStyles((theme) => ({
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: "#fff",
  },
}));

const AuthContext = createContext({} as any);

const FullPageSpinner = () => {
  const classes = useStyles();
  return (
    <Backdrop className={classes.backdrop} open>
      <CircularProgress color="inherit" />
    </Backdrop>
  );
};

function AuthProvider(props) {
  const [user, setUser] = useLocalStorage<IUser>("user");
  const [accessToken, setAccessToken] = useLocalStorage<string>(
    "acesss_token",
    null
  );
  const router = useRouter();
  const { t } = useTranslation();

  const anonymousLoginRoutes = [
    "/",
    "/login",
    "/register",
    "/forgot",
    "/users/set_password",
    "/about",
    "/contact",
    "/welcome",
  ];

  useEffect(() => {
    console.log(router.route);
    if (
      (!accessToken || !user) &&
      !anonymousLoginRoutes.includes(router.route)
    ) {
      setUser(null);
      router.push("/signin");
    }
  }, [user, accessToken, router.route]);

  const login = async ({ username, password }) => {
    const loginResponse = {
      success: false,
      message: t("errorOnLogin"),
    };
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
        setAccessToken(access_token);
        const logged = await callMe(access_token);
        if (logged) {
          loginResponse.success = true;
          loginResponse.message = t("successfulLogin");
        }
      }
      return loginResponse;
    } catch (error) {
      const { response } = error;
      loginResponse.message += Array.isArray(response?.data?.detail)
        ? t(response?.data?.detail[0].type.replace("value_error.", "invalid_"))
        : response?.data?.detail || response.status;

      return loginResponse;
    }
  };

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
      setUser(null);
      router.push("/");
      return false;
    }
  };

  const register = async (payload) => {
    const registrationResponse = {
      success: false,
      message: t("errorOnRegistration"),
    };
    try {
      const { data, status } = await axios.post(
        `${process.env.API_URL}/register`,
        payload
      );
      if (status === 200) {
        const { access_token, ...userData } = data;
        setAccessToken(access_token);
        setUser(userData);
        registrationResponse.success = true;
        registrationResponse.message = t("youAreNowRegistered");
      }
      return registrationResponse;
    } catch (error) {
      const { response } = error;

      registrationResponse.message += Array.isArray(response?.data?.detail)
        ? t(response?.data?.detail[0].type.replace("value_error.", "invalid_"))
        : response?.data?.detail || response.status;

      return registrationResponse;
    }
  };

  const logout = () => {
    setUser(null);

    router.push("/");
  };
  return (
    <AuthContext.Provider
      value={{ user, accessToken, login, register, logout }}
      {...props}
    />
  );
}
const useAuth = () => useContext(AuthContext);
export { AuthProvider, useAuth };
