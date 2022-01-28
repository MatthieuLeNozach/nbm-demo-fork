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

export interface StatisticsSpeciesItemProps {
  id: number;
  name: string;
  total: number;
  totalUser?: number
}

const StatisticsSpeciesItem: FC<StatisticsSpeciesItemProps> = ({
  id, name, total, totalUser
}) => {
  const classes = useStyles();

  return (
    <ListItem button>
      <Grid container className={classes.root}>
        <Grid item className={classes.fixed}>
          {id}
        </Grid>
        <Grid item xs>
          {name}
        </Grid>
        <Grid item className={classes.fixed}>
          <Typography align="right">{total}</Typography>
        </Grid>
        <Grid item className={classes.fixed}>
          <Typography align="right">{totalUser}</Typography>
        </Grid>
      </Grid>
    </ListItem>
  );
};

export default StatisticsSpeciesItem;
