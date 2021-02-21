import { Button, Grid, Container, Box } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import { theme } from "../theme/index";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import Dashboard from "../components/Dashboard/index";
import { useTranslation } from "react-i18next";

const useStyles = makeStyles((theme) => ({
  image: {
    height: "100vh",
    backgroundImage: 'url("/images/jackson-hendry-eodA_8CTOFo-unsplash.jpg")',
    backgroundRepeat: "no-repeat",
    backgroundSize: "cover",
    backgroundPosition: "center",
    backgroundAttachment: "fixed",
    //filter: "contrast(0.7)",
    position: "relative",
  },
  container: {
    height: "100%",
  },
  button1: {
    position: "absolute",
    right: "5rem",
    top: "5rem",
    backgroundColor: "rgba(7, 33, 54, 1)",
    color: "#FFFFFF",
  },
  button2: {
    position: "static",
    width: "199px",
    height: "80px",
    left: "0px",
    top: "0px",
    textAlign: "center",
    letterSpacing: "0.46px",
    margin: "0px 10px",
    backgroundColor: "rgba(103, 143, 175, 1)",
    color: "#FFFFFF",
    //fontFamily: "Roboto",
    fontStyle: "normal",
    fontSize: "15px",
    lineHeight: "26px",
  },
  button3: {
    position: "static",
    width: "199px",
    height: "80px",
    left: "0px",
    top: "0px",
    textAlign: "center",
    letterSpacing: "0.46px",
    margin: "0px 10px",
    backgroundColor: "rgba(103, 143, 175, 1)",
    color: "#FFFFFF",
    fontFamily: "Roboto",
    fontStyle: "normal",
    fontSize: "15px",
    lineHeight: "26px",
  },
}));

const WelcomePage = () => {
  const classes = useStyles(theme);
  const { t } = useTranslation();

  return (
    <Paper className={classes.image}>
      <Button variant="contained" className={classes.button1}>
        {t("signIn")}
      </Button>
      <Container className={classes.container}>
        <Grid
          className={classes.container}
          container
          direction="column"
          justify="center"
          alignItems="center"
        >
          <Grid item>
            <Typography variant="h4">{t("welcomeOnNBM")}</Typography>
          </Grid>
          <Grid item>
            <Box m={10}></Box>
          </Grid>
          <Grid item>
            <Dashboard></Dashboard>
          </Grid>
          <Grid item>
            <Box m={10}></Box>
          </Grid>
          <Grid item>
            <Grid container>
              <Grid item>
                <Button variant="contained" className={classes.button2}>
                  {t("exploreRecordings")}
                </Button>
              </Grid>
              <Grid item>
                <Button variant="contained" className={classes.button3}>
                  {t("addNewRecordings")}
                </Button>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Container>
    </Paper>
  );
};

export default WelcomePage;

/*  lineHeight: 26px,
    textAlign: center,
    letterSpacing: 0.46px,
    textTransform: uppercase, */
