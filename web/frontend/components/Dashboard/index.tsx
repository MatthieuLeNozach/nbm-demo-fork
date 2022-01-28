import React from "react";
import { Grid, makeStyles, Box } from "@material-ui/core";
import { theme } from "@/theme";
import Bird from "../Icon/Bird";
import Clock from "../Icon/Clock";
import Annotation from "../Icon/Annotation";
import Site from "../Icon/Site";
import User from "../Icon/User";
import Record from "../Icon/Record";
import { useTranslation } from "react-i18next";
import Item from "./Item";

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
});

type Props = {
  mediae: number;
  medialabels: number;
  species: number;
  sites: number;
  users?: number | null;
  annotatedSeconds?: number | null;
};

const Dashboard: React.FC<Props> = ({
  mediae = 0,
  medialabels = 0,
  species = 0,
  sites = 0,
  users = null,
  annotatedSeconds = null,
}: Props) => {
  const classes = useStyles();
  const { t } = useTranslation();

  let annotatedHours = null;
  if (annotatedSeconds) {
    const hours = Math.floor(annotatedSeconds / 3600);
    const minutes = Math.floor((annotatedSeconds % 3600) / 60);
    const seconds = Math.floor((annotatedSeconds % 3600) % 60);
    annotatedHours = hours + ":" + minutes + ":" + seconds;
  }

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
      icon: <Clock />,
      total: annotatedHours,
      label: t("annotatedHours"),
    },
    {
      icon: <Bird />,
      total: species,
      label: t("species"),
      href: "/statistics/species",
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
          .filter((item) => item.total !== null)
          .map((item) => (
            <Item
              key={item.label}
              label={item.label}
              total={item.total}
              icon={item.icon}
              href={item.href}
            />
          ))}
      </Grid>
    </Box>
  );
};

export default Dashboard;
