import React, { useState } from "react";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import { theme } from "@/theme";
import DoveSvg from "@/assets/svgs/DoveSvg";
import SwallowSvg from "@/assets/svgs/SwallowSvg";
import { useTranslation } from "react-i18next";
import { useRouter } from "next/router";
import axios from "axios";
import Link from "@material-ui/core/Link";
import { NextPage } from "next";
import { Alert } from "@material-ui/lab";

const useStyles = makeStyles({
  root: {
    height: "100vh",
    color: theme.palette.primary.main,
  },
  image: {
    backgroundImage: 'url("/images/jackson-hendry-eodA_8CTOFo-unsplash.jpg")',
    backgroundRepeat: "no-repeat",
    backgroundColor: theme.palette.background.default,
    backgroundSize: "cover",
    backgroundPosition: "center",
    position: "relative",
  },
  titleNBM: {
    position: "absolute",
    left: "50%",
    top: "50%",
    transform: "translate(-50%, -50%)",
    color: "white",
  },
  rightPanel: {
    position: "relative",
    backgroundColor: theme.palette.background.default,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
  },
  paper: {
    width: "100%",
    margin: theme.spacing(8, 4),
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: "80%", // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  button: {
    marginTop: 10,
  },
  passwordUpdatedContainer: {
    textAlign: "center",
  },
  hasTextWhite: {
    color: "white",
  },
  paragraph: {
    margin: 20,
  },
});

const ResetPasswordPage: NextPage = () => {
  const { t } = useTranslation();
  const classes = useStyles(theme);
  const router = useRouter();
  const { token } = router.query;

  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [confirmPassword, setConfirmPassword] = useState<string>("");
  const [passwordsAreDifferent, setPasswordsAreDifferent] = useState<boolean>(
    false
  );
  const [successResponse, setSuccessResponse] = useState<boolean>(false);
  const [errorResponse, setErrorResponse] = useState<boolean>(false);

  const responseCallback = (response) => {
    if (response.status === 200) {
      setSuccessResponse(true);
    } else {
      setErrorResponse(true);
    }
  };

  const changePassword = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setPasswordsAreDifferent(true);
      return;
    }
    axios
      .post(`${process.env.API_URL}/reset-password/`, {
        token: token.toString(),
        new_password: password,
      })
      .then(responseCallback)
      .catch(() => {
        setErrorResponse(true);
      });
  };

  const sendPasswordMail = async (e) => {
    e.preventDefault();

    axios
      .post(`${process.env.API_URL}/password-recovery/${email}`, {})
      .then(responseCallback)
      .catch(() => {
        setErrorResponse(true);
      });
  };

  return (
    <Grid container component="main" className={classes.root}>
      <CssBaseline />
      <Grid item xs={false} sm={4} md={6} className={classes.image}>
        <Typography component="h1" variant="h1" className={classes.titleNBM}>
          NBM
        </Typography>
      </Grid>
      <Grid
        item
        xs={12}
        sm={8}
        md={6}
        component={Paper}
        elevation={6}
        square
        className={classes.rightPanel}
      >
        <div className={classes.paper}>
          <Typography
            component="h1"
            variant="h5"
            className={classes.hasTextWhite}
          >
            {t("forgottenPassword")}
          </Typography>
          {errorResponse && <div>{t("errorOccurred")}</div>}

          {token && successResponse && (
            <div className={classes.passwordUpdatedContainer}>
              <div className={classes.paragraph}>
                {t("passwordSuccessfullyUpdated")}
              </div>
              <Button
                variant="contained"
                className={classes.button}
                color="primary"
                onClick={() => router.push("/signin")}
              >
                {t("signIn")}
              </Button>
            </div>
          )}
          {token && !successResponse && (
            <form
              className={classes.form}
              onSubmit={changePassword}
              autoComplete="off"
            >
              {passwordsAreDifferent && (
                <Alert severity="warning">passwordsAreDifferent</Alert>
              )}
              <TextField
                color="secondary"
                variant="outlined"
                margin="normal"
                required
                fullWidth
                name="password"
                label={t("common.password")}
                onChange={(e) => {
                  setPassword(e.target.value);
                  if (confirmPassword.length) {
                    setPasswordsAreDifferent(
                      e.target.value !== confirmPassword
                    );
                  }
                }}
                type="password"
                id="password"
                autoComplete="current-password"
              />
              <TextField
                color="secondary"
                variant="outlined"
                margin="normal"
                required
                fullWidth
                name="passwordConfirmation"
                label={t("common.confirmPassword")}
                onChange={(e) => {
                  setConfirmPassword(e.target.value);
                  setPasswordsAreDifferent(password !== e.target.value);
                }}
                type="password"
                id="passwordConfirmation"
                autoComplete="current-password"
              />
              <Button
                type="submit"
                variant="contained"
                color="primary"
                className={classes.button}
              >
                {t("common.updatePassword")}
              </Button>
            </form>
          )}

          {!token && successResponse && (
            <div className={classes.paragraph}>{t("passwordEmailSent")}</div>
          )}
          {!token && !successResponse && (
            <form className={classes.form} onSubmit={sendPasswordMail}>
              <TextField
                color="secondary"
                variant="outlined"
                margin="normal"
                required
                fullWidth
                id="email"
                label={t("email")}
                name="email"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoFocus
              />
              <Button
                type="submit"
                className={classes.button}
                variant="contained"
                color="primary"
              >
                {t("common.sendPasswordEmail")}
              </Button>

              <Grid container direction="column" alignItems="center">
                <Grid item className={classes.button}>
                  <Link
                    className={classes.button}
                    href="/signIn"
                    variant="body2"
                  >
                    {t("signIn")}
                  </Link>
                </Grid>
                <Grid item>
                  <Link
                    className={classes.button}
                    href="/register"
                    variant="body2"
                  >
                    {t("signUp")}
                  </Link>
                </Grid>
              </Grid>
            </form>
          )}
        </div>
        <DoveSvg
          style={{
            position: "absolute",
            top: "2rem",
            right: "4rem",
            width: "6rem",
            height: "6rem",
          }}
        />
        <SwallowSvg
          style={{
            position: "absolute",
            bottom: "4rem",
            left: "4rem",
            width: "6rem",
            height: "6rem",
          }}
        />
      </Grid>
    </Grid>
  );
};

export default ResetPasswordPage;
