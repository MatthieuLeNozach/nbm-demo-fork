import React from "react";
import { ThemeProvider, useTheme } from "@material-ui/core/styles";
import WelcomePage from "./welcome";
import { theme } from "../theme/index";
import { useTranslation } from "react-i18next";

const Home = () => {
  const { t } = useTranslation();
  return (
    <ThemeProvider theme={theme}>
      <WelcomePage />
      {/* <div style={{ color: theme.palette.primary.main }}>{hello}</div>
      <Button name="Click Me" color="primary" /> */}
    </ThemeProvider>
  );
};

export default Home;
