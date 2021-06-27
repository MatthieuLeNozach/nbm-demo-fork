import LayoutBase from "@/components/layout/base";
import { Button, Grid, Typography } from "@material-ui/core";
import { useTranslation } from "react-i18next";
import { useRouter } from "next/router";
import { NextPage } from "next";
import CustomPagination from "@/components/Pagination";
import { useState } from "react";
import { Media } from "@/models/media";

const RecordingsPage: NextPage = () => {
  const { t } = useTranslation();
  const router = useRouter();
  const [mediaeList, setMediaeList] = useState<Array<Media>>([]);
  const [selectedMediae] = useState<Array<Media>>([]);
  const { mine } = router.query;

  const downloadMediae = () => {
    window.open(`${process.env.API_URL}/utils/download`, "_blank");
  };

  return (
    <>
      <LayoutBase>
        <Grid
          container
          direction="column"
          justify="center"
          alignItems="center"
          spacing={4}
        >
          <Grid item>Explorer les enregistrements</Grid>
          <Grid item>Filtres - A venir</Grid>
          <Grid container direction="row" justify="center" alignItems="center">
            <Grid
              container
              direction="column"
              justify="flex-start"
              alignItems="flex-start"
              xs={7}
            >
              CARTO
            </Grid>
            <Grid
              container
              direction="column"
              justify="flex-start"
              alignItems="center"
              xs={5}
              spacing={1}
            >
              {!Array.isArray(mediaeList) ? (
                <Grid item>
                  <Typography variant="h4">Chargement en cours</Typography>
                </Grid>
              ) : mediaeList.length === 0 ? (
                <Grid item>
                  <Typography variant="h4">Aucun enregistrement</Typography>
                </Grid>
              ) : (
                mediaeList.map((media) => (
                  <Grid
                    key={media.id}
                    item
                    container
                    direction="row"
                    justify="flex-end"
                    alignItems="center"
                    spacing={2}
                    onClick={() => router.push(`recordings/${media.id}`)}
                  >
                    <Grid item sm={6}>
                      {media.file_source}
                    </Grid>
                    <Grid item sm={5}>
                      {new Date(media.begin_date).toString()}
                    </Grid>
                    <Grid item sm={1}>
                      {media.medialabels_count}
                    </Grid>
                  </Grid>
                ))
              )}
              <Grid item>
                <CustomPagination
                  endpoint={"mediae"}
                  numberByPage={10}
                  personal={!!mine}
                  onListChange={setMediaeList}
                />
              </Grid>
              <Grid
                container
                direction="row"
                justify="center"
                alignItems="center"
              >
                <Button variant="contained" onClick={downloadMediae}>
                  {selectedMediae.length
                    ? t("downloadSelection")
                    : t("fullDownload")}
                </Button>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </LayoutBase>
    </>
  );
};

export default RecordingsPage;
