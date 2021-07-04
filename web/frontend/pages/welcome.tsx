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
import { NextPage } from "next";
import { Alert } from "@material-ui/lab";

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
  alertBox: {
    marginTop: 15,
    alignItems: "center",
    whiteSpace: "pre-line",
  },
});

const WelcomePage: NextPage = () => {
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
            <Alert severity="info" className={classes.alertBox}>
              {t("welcomeTextPart1")} <br />
              {t("welcomeTextPart2")}{" "}
              <a
                rel="noreferrer"
                target="_blank"
                href="https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration"
              >
                https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration
              </a>{" "}
              <br />
              {t("welcomeTextPart3")}
            </Alert>
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
                onClick={() => router.push("/new-recording")}
              >
                {t("addNewRecordings")}
              </Button>
            </Grid>
          </Grid>
          <Grid
            item
            container
            direction="column"
            justify="space-around"
            alignItems="center"
          >
            <Grid item>
              <Typography align="center">
                Contactez-nous:{" "}
                <a href="mailto:pajot.adrien@wanadoo.fr">
                  pajot.adrien@wanadoo.fr
                </a>
              </Typography>
            </Grid>
            <Grid item>
              <Typography align="center">
                Rejoindre le groupe de discussion sur le projet:{" "}
                <a
                  rel="noreferrer"
                  target="_blank"
                  href="https://discord.gg/95SNguK3tP"
                >
                  https://discord.gg/95SNguK3tP
                </a>
              </Typography>
            </Grid>
          </Grid>
        </Grid>
      </Container>
      <Paper className={classes.backgroundImage} />
    </div>
  );
};

export default WelcomePage;
