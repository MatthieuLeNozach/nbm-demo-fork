import useSWR, { SWRConfig } from "swr";
import { useAuthActions } from "use-eazy-auth";
import Auth from "use-eazy-auth";
import axios from "axios";

const loginCall = async ({ username, password }) => {
  try {
    const { data, status } = await axios.post(
      "http://localhost/api/v1/login/access-token",
      {
        data: {
          username: username,
          password: password,
        },
      }
    );
    if (status === 200) {
      const { access_token } = data;
      return access_token;
    }
  } catch (error) {
    return "Unauthorized";
  }
};

const meCall = async (token: string) => {
  try {
    const { data, status } = await axios.get(
      "http://localhost/api/v1/users/me",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    if (status === 200) {
      return data;
    }
  } catch (error) {
    return "Unauthorized";
  }
};

const AuthProvider = ({ children }) => {
  const { callAuthApiPromise } = useAuthActions();
  return (
    <Auth
      loginCall={loginCall}
      meCall={meCall}
      storageBackend={localStorage}
      storageNamespace="nbm-auth"
    >
      <SWRConfig
        value={{
          fetcher: (...args) =>
            callAuthApiPromise(
              (token) => (url, options) =>
                fetch(url, {
                  ...options,
                  headers: {
                    ...options?.headers,
                    Authorization: `Bearer ${token}`,
                  },
                })
                  // NOTE: use-eazy-auth needs a Rejection with shape:
                  // { status: number }
                  .then((res) => (res.ok ? res.json() : Promise.reject(res))),
              ...args
            ),
        }}
      >
        {children}
      </SWRConfig>
    </Auth>
  );
};

export default AuthProvider;
