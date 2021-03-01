import React from "react";
import { Grid, makeStyles, Box } from "@material-ui/core";
import { theme } from "@/theme";
import Bird from "../Icon/Bird";
import Annotation from "../Icon/Annotation";
import Site from "../Icon/Site";
import User from "../Icon/User";
import Record from "../Icon/Record";
import { useTranslation } from "react-i18next";

const useStyles = makeStyles({
  dashboard: {
    backgroundColor: theme.palette.secondary.main,
    borderRadius: "5px",
    textAlign: "left",
    color: theme.palette.secondary.contrastText,
  },
  grid: {
    "& > div:last-child": {
      borderRight: 0,
    },
  },
  item: {
    [theme.breakpoints.up("md")]: {
      borderRight: "1px solid #ddd",
    },
  },
  box: {
    minWidth: "6.5rem",
  },
});

const Dashboard = () => {
  const classes = useStyles();
  const { t } = useTranslation();
  // TODO replace test par un call a l'api
  const test = 123;

  const items = [
    {
      icon: <Record />,
      total: test,
      label: t("recordings"),
    },
    {
      icon: <Annotation />,
      total: test,
      label: t("labels"),
    },
    {
      icon: <Bird />,
      total: test,
      label: t("species"),
    },
    {
      icon: <Site />,
      total: test,
      label: t("sites"),
    },
    {
      icon: <User />,
      total: test,
      label: t("contributors"),
    },
  ];

  return (
    <Box my={5} p={5} className={classes.dashboard}>
      <Grid
        className={classes.grid}
        container
        alignItems="center"
        direction="row"
        justify="center"
        spacing={5}
      >
        {items.map((item) => (
          <Grid className={classes.item} item key={`${item.label}`}>
            <Grid
              className={classes.box}
              container
              direction="column"
              alignItems="center"
            >
              <Grid item>{item.icon}</Grid>
              <Grid item> {item.total} </Grid>
              <Grid item>{item.label} </Grid>
            </Grid>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Dashboard;
