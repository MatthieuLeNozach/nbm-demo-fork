import { FC } from "react";
import { ListItem, Grid, makeStyles, Typography } from "@material-ui/core";

const useStyles = makeStyles({
  root: {
    gap: "10px",
  },
  fixed: {
    width: 60,
  },
});

const StatisticsSpeciesHeader: FC = ({}) => {
  const classes = useStyles();

  return (
    <ListItem>
      <Grid container className={classes.root}>
        <Grid item className={classes.fixed}>
          <Typography>Code</Typography>
        </Grid>
        <Grid item xs>
          <Typography>Specie</Typography>
        </Grid>
        <Grid item className={classes.fixed}>
          <Typography align="right" noWrap>
            Total
          </Typography>
        </Grid>
        <Grid item className={classes.fixed}>
          <Typography align="right" noWrap>
            Total user
          </Typography>
        </Grid>
      </Grid>
    </ListItem>
  );
};

export default StatisticsSpeciesHeader;
