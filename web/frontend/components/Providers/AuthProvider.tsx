import { createContext, useContext, useEffect } from "react";
import Backdrop from "@material-ui/core/Backdrop";
import CircularProgress from "@material-ui/core/CircularProgress";
import { makeStyles } from "@material-ui/core/styles";
import useLocalStorage from "@/hooks/useLocalStorage";
import { useRouter } from "next/router";
import axios from "axios";

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
  const allowedRoutes = [
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
    if (!accessToken && !user && !allowedRoutes.includes(router.route)) {
      localStorage.clear();
      router.push("/signin");
    }
  }, [user, accessToken]);

  const login = async ({ username, password }) => {
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
        "http://localhost:8999/api/v1/login/access-token",
        payload,
        config
      );
      if (status === 200) {
        const { access_token } = data;
        setAccessToken(access_token);
        callMe(access_token);
      }
    } catch (error) {
      const { response } = error;
      const { data, status } = response;
      if (status === 400) {
        return data;
      }
    }
  };

  const callMe = async (token) => {
    try {
      const { data, status } = await axios.get(
        "http://localhost:8999/api/v1/users/me",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      if (status === 200) {
        setUser(data);
      }
    } catch (error) {
      const { response } = error;
      const { data, status } = response;
      if (status === 403) {
        return data;
      } else {
        console.log(status);
        console.log(data);
        localStorage.clear();
        router.push("/");
      }
    }
  };

  const register = async (payload) => {
    try {
      const { data, status } = await axios.post(
        "http://localhost:8999/api/v1/register",
        payload
      );
      if (status === 200) {
        const { access_token, ...userData } = data;
        setAccessToken(access_token);
        setUser(userData);
      }
    } catch (error) {
      const { response } = error;
      const { data, status } = response;
      if (status === 400) {
        return data;
      }
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.clear();
    router.push("/");
  };
  return (
    <AuthContext.Provider
      value={{ user, accessToken, login, logout }}
      {...props}
    />
  );
}
const useAuth = () => useContext(AuthContext);
export { AuthProvider, useAuth };
