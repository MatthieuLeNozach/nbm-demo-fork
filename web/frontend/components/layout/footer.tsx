import { Box, Container, Grid, makeStyles } from "@material-ui/core";
import { theme } from "@/theme/index";

const useStyles = makeStyles({
  footer: {
    backgroundColor: theme.palette.primary.main,
    height: 50,
  },
});

const LayoutFooter = () => {
  const classes = useStyles();

  return (
    <Grid container alignItems="flex-end" className={classes.footer}>
      <Box m={2}>Footer</Box>
    </Grid>
  );
};

export default LayoutFooter;
