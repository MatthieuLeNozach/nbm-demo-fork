import { FC } from "react";
import { List, makeStyles } from "@material-ui/core";

const useStyles = makeStyles({
  root: {
    background: "rgba(255, 255, 255, .2)",
  },
});

const StatisticsSpeciesList: FC = ({ children }) => {
  const classes = useStyles();

  return <List className={classes.root}>{children}</List>;
};

export default StatisticsSpeciesList;
