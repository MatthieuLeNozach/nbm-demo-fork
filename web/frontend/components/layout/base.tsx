import { Container, Grid, makeStyles } from "@material-ui/core";
import LayoutHeader from "@/components/layout/header";
import LayoutFooter from "@/components/layout/footer";

const useStyles = makeStyles({
  root: {
    height: "100vh",
  },
});

const LayoutBase = ({ children }) => {
  
  const classes = useStyles();
  return (
    <>
    <Grid container direction="column" justify="space-between" alignItems="stretch" className={classes.root}>
      <Grid container alignItems="flex-start"><LayoutHeader /></Grid>
      <Container fixed>{children}</Container>
      <Grid container alignItems="flex-end"><LayoutFooter /></Grid>
    </Grid>
    </>
  );
};

export default LayoutBase;
