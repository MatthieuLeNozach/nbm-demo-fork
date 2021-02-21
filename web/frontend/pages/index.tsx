import React from "react";
import { ThemeProvider, useTheme } from "@material-ui/core/styles";
import LoginPage from "./LoginPage";
import { theme } from "../theme/index";
import { useTranslation } from "react-i18next";

const Home = () => {
  const hello = "Hello";
  const { t } = useTranslation();
  return (
    <ThemeProvider theme={theme}>
      <LoginPage />
      {t("welcome")}
      {/* <div style={{ color: theme.palette.primary.main }}>{hello}</div>
      <Button name="Click Me" color="primary" /> */}
    </ThemeProvider>
  );
};

export default Home;
