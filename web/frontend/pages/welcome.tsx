import React from "react";
import { Button, Grid, Container } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import { theme } from "@/theme";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import Dashboard from "../components/Dashboard/index";
import { useTranslation } from "react-i18next";
import { useRouter } from "next/router";
import useSWR from "swr";

const useStyles = makeStyles({
  backgroundImage: {
    position: "fixed",
    top: 0,
    left: 0,
    minHeight: "100vh",
    minWidth: "100vw",
    opacity: "0.7",
    backgroundImage: 'url("/images/jackson-hendry-eodA_8CTOFo-unsplash.jpg")',
    backgroundRepeat: "no-repeat",
    backgroundSize: "cover",
    backgroundPosition: "center",
    backgroundAttachment: "fixed",
  },
  globalWrapper: {
    backgroundColor: "white",
  },
  globalGrid: {
    position: "relative",
    minHeight: "100vh",
    zIndex: 1,
  },
  signInButton: {
    [theme.breakpoints.up("sm")]: {
      position: "absolute",
      right: "2rem",
      top: "2rem",
    },
    position: "relative",
    zIndex: 2,
    backgroundColor: "rgba(7, 33, 54, 1)",
    color: "#FFFFFF",
    margin: "10px",
  },
  bottomButtons: {
    fontSize: "15px",
    lineHeight: "26px",
    color: "#FFFFFF",
    backgroundColor: theme.palette.action.active,
    margin: "10px 25px",
    width: "243px",
    minHeight: "68px",
    textAlign: "center",
    // fontFamily: "Roboto",
  },
});

const WelcomePage = () => {
  const classes = useStyles();
  const { t } = useTranslation();
  const router = useRouter();
  const { data: globalCount } = useSWR("/utils/count");

  return (
    <div className={classes.globalWrapper}>
      <Container>
        <Grid
          item
          container
          direction="row"
          justify="center"
          alignItems="center"
        >
          <Grid item>
            <Button
              variant="contained"
              className={classes.signInButton}
              onClick={() => router.push("/signin")}
            >
              {t("signIn")}
            </Button>
          </Grid>
        </Grid>
        <Grid
          className={classes.globalGrid}
          container
          direction="column"
          justify="center"
          alignItems="center"
        >
          <Grid item>
            <Typography variant="h4">{t("welcomeOnNBM")}</Typography>
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
          <Grid
            item
            container
            direction="row"
            justify="center"
            alignItems="center"
          >
            <Grid item>
              <Button
                variant="contained"
                className={classes.bottomButtons}
                onClick={() => router.push("/signin")}
              >
                {t("exploreRecordings")}
              </Button>
            </Grid>
            <Grid item>
              <Button
                variant="contained"
                className={classes.bottomButtons}
                onClick={() => router.push("/newrecording")}
              >
                {t("addNewRecordings")}
              </Button>
            </Grid>
          </Grid>
        </Grid>
      </Container>
      <Paper className={classes.backgroundImage} />
    </div>
  );
};

export default WelcomePage;
