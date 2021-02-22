import { createContext, useContext } from "react";
import { useAuth } from "@/components/Providers/AuthProvider";

const UserContext = createContext({} as any);

const UserProvider = (props) => (
  <UserContext.Provider value={useAuth().user} {...props} />
);
const useUser = () => useContext(UserContext);

export { UserProvider, useUser };
