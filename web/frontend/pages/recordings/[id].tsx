import LayoutBase from "@/components/layout/base";
import { Grid } from "@material-ui/core";
import { useTranslation } from "react-i18next";
import { useAuth } from "@/components/Providers/AuthProvider";
import useSWR from "swr";
import { useRouter } from "next/router";
import Typography from "@material-ui/core/Typography";
import { NextPage } from "next";

const RecordingPage: NextPage = () => {
  const { t } = useTranslation();
  const router = useRouter();
  const { accessToken } = useAuth();
  const { id } = router.query;
  const { data: media } = useSWR(id ? [`/mediae/${id}`, accessToken] : null);
  return (
    <>
      <LayoutBase>
        {!media ? (
          <div>{t("loading")}</div>
        ) : (
          <Grid
            container
            direction="column"
            alignItems="flex-start"
            spacing={1}
          >
            <Grid item>
              <Typography variant="h6">{t("media_information")}</Typography>
            </Grid>
            <Grid item>
              {t("media_source")}: {media.file_source}
            </Grid>
            <Grid item>
              {t("media_date")}: {media.begin_date}
            </Grid>
            <Grid item>
              {t("media_duration")}: {media.duration}
            </Grid>
            {Array.isArray(media.medialabels) &&
            media.medialabels.length === 0 ? (
              <Grid item>{t("no_media_label")}</Grid>
            ) : (
              <Grid
                item
                container
                direction="column"
                alignItems="flex-start"
                spacing={1}
              >
                <Grid item>
                  <Typography variant="h6">
                    {t("invalid_media_labels")}
                  </Typography>
                </Grid>
                {Array.isArray(media.medialabels) &&
                  media.medialabels
                    .filter((medialabel) => !medialabel.label)
                    .map((medialabel) => (
                      <Grid
                        item
                        container
                        direction="row"
                        alignItems="center"
                        spacing={1}
                        key={medialabel.id}
                      >
                        <Grid item sm={4}>
                          {t("medialabel_from")}: {medialabel.begin_time}
                        </Grid>
                        <Grid item sm={4}>
                          {t("medialabel_to")}: {medialabel.end_time}
                        </Grid>
                        <Grid item sm={4}>
                          {t("medialabel_invalid_label_text")}:
                          {medialabel.invalid_label_text}
                        </Grid>
                      </Grid>
                    ))}
                <Grid item>
                  <Typography variant="h6">
                    {t("valid_media_labels")}
                  </Typography>
                </Grid>
                {Array.isArray(media.medialabels) &&
                  media.medialabels
                    .filter((medialabel) => medialabel.label)
                    .map((medialabel) => (
                      <Grid
                        item
                        container
                        direction="row"
                        alignItems="center"
                        spacing={1}
                        key={medialabel.id}
                      >
                        <Grid item sm={4}>
                          {t("medialabel_from")}: {medialabel.begin_time}
                        </Grid>
                        <Grid item sm={4}>
                          {t("medialabel_to")}: {medialabel.end_time}
                        </Grid>
                        <Grid item sm={4}>
                          {t("medialabel_label_name")}:{medialabel.label.name}
                        </Grid>
                      </Grid>
                    ))}
              </Grid>
            )}
          </Grid>
        )}
      </LayoutBase>
    </>
  );
};

export default RecordingPage;
