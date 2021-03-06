import { Grid, makeStyles, Button, Box } from "@material-ui/core";
import { theme } from "@/theme";
import { useRouter } from "next/router";
import { useTranslation } from "react-i18next";
import { useAuth } from "@/components/Providers/AuthProvider";

const useStyles = makeStyles({
  header: {
    backgroundColor: theme.palette.primary.main,
  },
});

const LayoutHeader = () => {
  const classes = useStyles();
  const router = useRouter();
  const { t } = useTranslation();
  const { logout } = useAuth();

  const handlerOnClickHome = () => {
    console.log("onClick handlerOnClickHome");
    router.push("/home");
  };

  return (
    <Grid container className={classes.header} alignItems="center">
      <Grid item md={6}>
        <Box ml={1}>
          <Button name="Home" onClick={handlerOnClickHome}>
            Nocturnal Bird Migration
          </Button>
        </Box>
      </Grid>
      <Grid item md={6}>
        <Box mr={1}>
          <Grid
            container
            direction="row"
            justify="flex-end"
            alignItems="center"
          >
            <Grid item>
              <Button name="Sign out" onClick={logout}>
                {t("logout")}
              </Button>
            </Grid>
          </Grid>
        </Box>
      </Grid>
    </Grid>
  );
};

export default LayoutHeader;
