import LayoutBase from "@/components/layout/base";
import { theme } from "@/theme";
import { Button, Grid, makeStyles } from "@material-ui/core";
import { useTranslation } from "react-i18next";
import { useRouter } from "next/router";
import Dashboard from "../components/Dashboard/index";
import Typography from "@material-ui/core/Typography";
import { useAuth } from "@/components/Providers/AuthProvider";
import useSWR from "swr";

const useStyles = makeStyles({
  bottomButton: {
    fontSize: "15px",
    lineHeight: "26px",
    color: "#FFFFFF",
    backgroundColor: theme.palette.primary.main,
    margin: "0 25px 25px",
    width: "243px",
    minHeight: "68px",
    textAlign: "center",
  },
  globalGrid: {
    minHeight: "60vh",
  },
  titleGrid: {
    margin: "30px 0",
  },
  dashboardTitle: {
    width: "500px",
    maxWidth: "100%",
    borderBottom: "1px solid white",
    textAlign: "center",
  },
});

const HomePage = () => {
  const classes = useStyles();
  const { t } = useTranslation();
  const router = useRouter();
  const { user, accessToken } = useAuth();
  const { data: globalCount } = useSWR(["/utils/count", accessToken]);
  const { data: personalCount } = useSWR([
    "/utils/personal-count",
    accessToken,
  ]);

  return (
    <>
      <LayoutBase>
        <Grid
          className={classes.globalGrid}
          container
          direction="column"
          justify="center"
          alignItems="center"
        >
          <Grid
            className={classes.titleGrid}
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
              <Typography variant="h4">
                {t("welcome") + " " + ((user && user.full_name) ?? "")}
              </Typography>
            </Grid>
          </Grid>
          <Grid item className={classes.dashboardTitle}>
            <Typography variant="h5">{t("generalStatistics")}</Typography>
          </Grid>
          <Grid item>
            {globalCount ? (
              <Dashboard
                mediae={globalCount.mediae}
                medialabels={globalCount.medialabels}
                species={globalCount.species}
                sites={globalCount.sites}
                users={globalCount.users}
                annotatedSeconds={globalCount.annotated_seconds}
              />
            ) : (
              <div>Données globales irrécupérables</div>
            )}
          </Grid>
          <Grid item className={classes.dashboardTitle}>
            <Typography variant="h5">{t("myStatistics")}</Typography>
          </Grid>
          <Grid item>
            {personalCount ? (
              <Dashboard
                mediae={personalCount.mediae}
                medialabels={personalCount.medialabels}
                species={personalCount.species}
                sites={personalCount.sites}
                annotatedSeconds={personalCount.annotated_seconds}
              />
            ) : (
              <div>Données globales irrécupérables</div>
            )}
          </Grid>
          <Grid
            item
            container
            direction="row"
            justify="center"
            alignItems="center"
          >
            <Button
              variant="contained"
              className={classes.bottomButton}
              onClick={() => router.push("/signin")}
            >
              {t("exploreRecordings")}
            </Button>
            <Button
              variant="contained"
              className={classes.bottomButton}
              onClick={() => router.push("/signin")}
            >
              {t("myRecordings")}
            </Button>
            <Button
              variant="contained"
              className={classes.bottomButton}
              onClick={() => router.push("/newrecording")}
            >
              {t("addNewRecordings")}
            </Button>
            <Button
              variant="contained"
              className={classes.bottomButton}
              onClick={() => router.push("/signin")}
            >
              {t("manageSites")}
            </Button>
          </Grid>
        </Grid>
      </LayoutBase>
    </>
  );
};

export default HomePage;
