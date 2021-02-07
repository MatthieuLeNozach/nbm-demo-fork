import React from "react";
import { ThemeProvider, useTheme } from "@material-ui/core/styles";
import { Button } from "../components/button";
import LoginPage from "./LoginPage";
import { theme } from '../theme/index';

const Home = () => {
  const hello = "Hello";
  return (
    <ThemeProvider theme={theme}>
      <LoginPage />
      {/* <div style={{ color: theme.palette.primary.main }}>{hello}</div>
      <Button name="Click Me" color="primary" /> */}
    </ThemeProvider>
  );
};

export default Home;
