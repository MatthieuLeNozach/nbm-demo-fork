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

interface StatisticsSpeciesHeaderProps {}

const StatisticsSpeciesHeader: FC<StatisticsSpeciesHeaderProps> = ({}) => {
  const classes = useStyles();
  const { user } = useAuth();

  return (
    <ListItem>
      <Grid container className={classes.root}>
        <Grid item className={classes.fixed}>
          <Typography>Code</Typography>
        </Grid>
        <Grid item xs>
          <Typography>Species</Typography>
        </Grid>
        <Grid item className={classes.fixed}>
          <Typography align="right" noWrap>
            Total
          </Typography>
        </Grid>
        {user && (
          <Grid item className={classes.fixed}>
            <Typography align="right" noWrap>
              Total user
            </Typography>
          </Grid>
        )}
      </Grid>
    </ListItem>
  );
};

export default StatisticsSpeciesHeader;
