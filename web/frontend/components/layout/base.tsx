import { Container, Grid, makeStyles, Theme } from "@material-ui/core";
import LayoutHeader from "@/components/layout/header";
import LayoutFooter from "@/components/layout/footer";
import { FC } from "react";

interface LayoutBaseProps {
  centered?: boolean;
}

const useStyles = makeStyles<Theme, LayoutBaseProps>({
  root: {
    height: "100vh",
    flexWrap: "nowrap",
    gap: "10px",
  },
  main: ({ centered }) => ({
    flex: centered ? 0 : 1,
  }),
});

const LayoutBase: FC<LayoutBaseProps> = ({ centered = true, children }) => {
  const classes = useStyles({ centered });

  return (
    <Grid
      container
      className={classes.root}
      direction="column"
      justify="space-between"
      alignItems="stretch"
    >
      <Grid item>
        <Grid container alignItems="flex-start">
          <LayoutHeader />
        </Grid>
      </Grid>
      <Grid item className={classes.main}>
        <Container fixed>{children}</Container>
      </Grid>
      <Grid item>
        <Grid container alignItems="flex-end">
          <LayoutFooter />
        </Grid>
      </Grid>
    </Grid>
  );
};

export default LayoutBase;
