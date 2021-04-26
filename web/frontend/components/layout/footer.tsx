import { Box, Grid, makeStyles } from "@material-ui/core";
import { theme } from "@/theme";
import React from "react";

const useStyles = makeStyles({
  footer: {
    backgroundColor: theme.palette.primary.main,
    height: 50,
  },
});

const LayoutFooter: React.FC = () => {
  const classes = useStyles();

  return (
    <Grid container alignItems="flex-end" className={classes.footer}>
      <Box m={2}>Footer</Box>
    </Grid>
  );
};

export default LayoutFooter;
