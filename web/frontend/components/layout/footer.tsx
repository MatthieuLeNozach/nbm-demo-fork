import { Typography, Grid, makeStyles } from "@material-ui/core";
import { theme } from "@/theme";
import React from "react";

const useStyles = makeStyles({
  footer: {
    backgroundColor: theme.palette.primary.main,
    minHeight: 50,
  },
});

const LayoutFooter: React.FC = () => {
  const classes = useStyles();

  return (
    <Grid
      container
      alignItems="center"
      justify="center"
      className={classes.footer}
    >
      <Grid
        container
        direction="column"
        alignItems="center"
        justify="center"
        wrap="wrap"
      >
        <Grid item>
          <Typography align="center">
            Contactez-nous:{" "}
            <a href="mailto:pajot.adrien@wanadoo.fr">pajot.adrien@wanadoo.fr</a>
          </Typography>
        </Grid>
        <Grid item>
          <Typography align="center">
            Rejoindre le groupe de discussion sur le projet:{" "}
            <a
              rel="noreferrer"
              target="_blank"
              href="https://discord.gg/95SNguK3tP"
            >
              https://discord.gg/95SNguK3tP
            </a>
          </Typography>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default LayoutFooter;
