import LayoutBase from "@/components/layout/base";
import { Grid, makeStyles } from "@material-ui/core";
import { useTranslation } from "react-i18next";
import { useAuth } from "@/components/Providers/AuthProvider";
import useSWR from "swr";
import { useRouter } from "next/router";
import Typography from "@material-ui/core/Typography";
import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import { NextPage } from "next";

const useStyles = makeStyles({
  mapContainer: {
    width: "100%",
    minWidth: "300px",
  },
});

const SitePage: NextPage = () => {
  const [isBrowser, setIsBrowser] = useState(false);
  useEffect(() => {
    setIsBrowser(true);
  }, []);

  const MapWithNoSSR = dynamic(() => import("../../components/MapWithNoSSR"), {
    ssr: false,
  });

  const classes = useStyles();
  const { t } = useTranslation();
  const router = useRouter();
  const { accessToken } = useAuth();
  const { id } = router.query;
  const { data: site } = useSWR(id ? [`/sites/${id}`, accessToken] : null);
  const position = {
    latitude: site ? site.latitude : 0,
    longitude: site ? site.longitude : 0,
  };

  return !isBrowser ? (
    <div>{t("loading")}</div>
  ) : (
    <>
      <LayoutBase>
        {!site ? (
          <div>{t("loading")}</div>
        ) : (
          <Grid
            container
            direction="column"
            alignItems="flex-start"
            spacing={1}
          >
            <Grid item>
              <Typography variant="h6">{t("site_information")}</Typography>
            </Grid>
            <Grid item>
              {t("site_name")}: {site.name}
            </Grid>
            <Grid item className={classes.mapContainer}>
              <MapWithNoSSR position={position} />
            </Grid>
          </Grid>
        )}
      </LayoutBase>
    </>
  );
};

export default SitePage;
