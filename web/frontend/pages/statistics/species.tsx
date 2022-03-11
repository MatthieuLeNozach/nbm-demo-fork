import { useRouter } from "next/router";
import { NextPage } from "next";
import {
  Grid,
  Button,
  Typography,
  Divider,
  makeStyles,
} from "@material-ui/core";
import LayoutBase from "@/components/layout/base";
import { useAuth } from "@/components/Providers/AuthProvider";
import useSWR from "swr";
import StatisticsSpeciesHeader from "@/components/Statistics/Species/Header";
import StatisticsSpeciesList from "@/components/Statistics/Species/List";
import StatisticsSpeciesItem from "@/components/Statistics/Species/Item";
import { useTranslation } from "react-i18next";


const useStyles = makeStyles((theme) => ({
  title: {
    fontSize: "xx-large",
  },
  [theme.breakpoints.up("sm")]: {
    title: {
      fontSize: "2rem",
    },
  },
}));

const StatisticsSpeciesPage: NextPage = () => {
  const router = useRouter();
  const classes = useStyles();
  const {t} = useTranslation()
  const { accessToken } = useAuth();
  const { data: species = [] } = useSWR(["/statistics/species_annotations", accessToken]);

  const handleGoToDashboard = () => {
    router.push("/home");
  };

  return (
    <LayoutBase centered={false}>
      <Grid container direction="column" spacing={2}>
        <Grid item>
          <Typography className={classes.title}>
            {t("StatisticsSpeciesPage_title")}
          </Typography>
        </Grid>
        <Grid item>
          <Grid container>
            <Grid item>
              <Button variant="outlined" onClick={handleGoToDashboard}>
                 {t("StatisticsSpeciesPage_backHome")}
              </Button>
            </Grid>
          </Grid>
        </Grid>
        <Grid item>
          <StatisticsSpeciesList>
            <StatisticsSpeciesHeader />
            <Divider />
            {species.map((s) => ( <StatisticsSpeciesItem total={s.total} name={s.name} id={s.id} />))}
          </StatisticsSpeciesList>
        </Grid>
      </Grid>
    </LayoutBase>
  );
};

export default StatisticsSpeciesPage;
