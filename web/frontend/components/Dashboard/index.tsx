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

const Dashboard = ({
  mediae = "N/A",
  medialabels = "N/A",
  species = "N/A",
  sites = "N/A",
  users,
}) => {
  const classes = useStyles();
  const { t } = useTranslation();

  const items = [
    {
      icon: <Record />,
      total: mediae,
      label: t("recordings"),
    },
    {
      icon: <Annotation />,
      total: medialabels,
      label: t("labels"),
    },
    {
      icon: <Bird />,
      total: species,
      label: t("species"),
    },
    {
      icon: <Site />,
      total: sites,
      label: t("sites"),
    },
    {
      icon: <User />,
      total: users,
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
        {items
          .filter((item) => typeof item.total !== "undefined")
          .map((item) => (
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
