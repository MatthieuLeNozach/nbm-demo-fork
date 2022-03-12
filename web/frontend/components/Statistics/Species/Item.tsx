import { FC } from "react";
import { ListItem, Grid, makeStyles, Typography } from "@material-ui/core";
import { useAuth } from "@/components/Providers/AuthProvider";

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
  total_by_user?: number | undefined;
}

const StatisticsSpeciesItem: FC<StatisticsSpeciesItemProps> = ({
  id,
  name,
  total,
  total_by_user,
}) => {
  const classes = useStyles();
  const { user } = useAuth();

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
        {user && (
          <Grid item className={classes.fixed}>
            <Typography align="right">{total_by_user}</Typography>
          </Grid>
        )}
      </Grid>
    </ListItem>
  );
};

export default StatisticsSpeciesItem;
