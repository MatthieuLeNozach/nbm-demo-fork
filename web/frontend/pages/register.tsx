import React, { useEffect, useState } from "react";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import Link from "@material-ui/core/Link";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import { theme } from "@/theme";
import DoveSvg from "@/assets/svgs/DoveSvg";
import SwallowSvg from "@/assets/svgs/SwallowSvg";
import { useTranslation } from "react-i18next";
import { useAuth } from "@/components/Providers/AuthProvider";
import { useRouter } from "next/router";

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
  submit: {
    margin: theme.spacing(3, 0, 2),
    width: "min-content",
  },
  hasTextWhite: {
    color: "white",
  },
});

const RegisterPage = () => {
  const { t } = useTranslation();
  const classes = useStyles(theme);
  const { register, user } = useAuth();
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirmation, setPasswordConfirmation] = useState("");

  useEffect(() => {
    if (user) {
      router.push("/home");
    }
  }, [user]);

  const handleCreateUser = (event) => {
    register({
      email: email,
      is_active: true,
      is_superuser: false,
      full_name: fullName,
      password: password,
      password_confirmation: passwordConfirmation,
    }).then((registrationResponse) => {
      alert(registrationResponse.message);
    });

    event.preventDefault();
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
            {t("registerOnNBM")}
          </Typography>
          <form className={classes.form} onSubmit={handleCreateUser}>
            <TextField
              color="secondary"
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="fullName"
              label={t("fullName")}
              name="fullName"
              autoComplete="current-fullName"
              autoFocus
              onChange={(event) => setFullName(event.target.value)}
            />
            <TextField
              color="secondary"
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="email"
              label={t("email")}
              name="login"
              autoComplete="email"
              autoFocus
              onChange={(event) => setEmail(event.target.value)}
            />
            <TextField
              color="secondary"
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="password"
              label={t("password")}
              type="password"
              id="password"
              autoComplete="current-password"
              onChange={(event) => setPassword(event.target.value)}
            />
            <TextField
              color="secondary"
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="confirmPassword"
              label={t("confirmPassword")}
              type="password"
              id="confirmPassword"
              autoComplete="current-password"
              onChange={(event) => setPasswordConfirmation(event.target.value)}
            />
            <Button
              type="submit"
              variant="contained"
              color="primary"
              className={classes.submit}
            >
              {t("register")}
            </Button>
            <Grid container direction="column" alignItems="center">
              <Grid item xs>
                <Link href="#" variant="body2">
                  {t("forgotPassword")}
                </Link>
              </Grid>
              <Grid item>
                <Link href="/signin" variant="body2">
                  {t("alreadyRegistered")}
                </Link>
              </Grid>
            </Grid>
          </form>
        </div>
        <DoveSvg
          style={{
            position: "absolute",
            top: "4rem",
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

export default RegisterPage;
