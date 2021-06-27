import LayoutBase from "@/components/layout/base";
import { Grid, Typography } from "@material-ui/core";
import { useRouter } from "next/router";
import { NextPage } from "next";
import CustomPagination from "@/components/Pagination";
import { useState } from "react";
import { Site } from "@/models/site";

const SitesPage: NextPage = () => {
  const router = useRouter();
  const { mine } = router.query;
  const [sitesList, setSitesList] = useState<Array<Site>>([]);

  return (
    <>
      <LayoutBase>
        <Grid
          container
          direction="column"
          justify="flex-start"
          alignItems="center"
          spacing={1}
        >
          {!Array.isArray(sitesList) ? (
            <Grid item>
              <Typography variant="h4">Chargement en cours</Typography>
            </Grid>
          ) : sitesList.length === 0 ? (
            <Grid item>
              <Typography variant="h4">Aucun site</Typography>
            </Grid>
          ) : (
            sitesList.map((site) => (
              <Grid
                key={site.id}
                item
                container
                direction="row"
                justify="flex-start"
                alignItems="center"
                spacing={2}
                onClick={() => router.push(`sites/${site.id}`)}
              >
                <Grid item sm={6}>
                  {site.name}
                </Grid>
              </Grid>
            ))
          )}
          <CustomPagination
            endpoint={"sites"}
            numberByPage={10}
            personal={!!mine}
            onListChange={setSitesList}
          />
        </Grid>
      </LayoutBase>
    </>
  );
};

export default SitesPage;
