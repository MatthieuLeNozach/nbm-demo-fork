import { ThemeProvider } from "@material-ui/core/styles";
import WelcomePage from "./welcome";
import { theme } from "@/theme";
import { NextPage } from "next";

const Home: NextPage = () => {
  return (
    <ThemeProvider theme={theme}>
      <WelcomePage />
      {/* <div style={{ color: theme.palette.primary.main }}>{hello}</div>
      <Button name="Click Me" color="primary" /> */}
    </ThemeProvider>
  );
};

export default Home;
