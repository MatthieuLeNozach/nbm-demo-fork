import { Button, Typography } from "@material-ui/core";
import { useAuth } from "@/components/Providers/AuthProvider";
import { useEffect } from "react";

const Authorized = () => {
  const { logout } = useAuth();

  return (
    <div>
      <Typography>Authorized!</Typography>
      <Button variant="outlined" color="secondary" onClick={logout}>
        Déconnexion
      </Button>
    </div>
  );
};

export default Authorized;
