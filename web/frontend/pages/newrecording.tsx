import LayoutBase from "@/components/layout/base";
import { useState } from "react";
import MediaUploadForm from "@/components/MediaUploadForm";
import Button from "@material-ui/core/Button";
import { useRouter } from "next/router";
import { SelectOption } from "@/models/utils";
import { MediaUploadResponse } from "@/models/media";
import { useTranslation } from "react-i18next";
import { Grid, Typography } from "@material-ui/core";

const NewRecordingPage = () => {
  const router = useRouter();
  const { t } = useTranslation();
  const [previouslyUsedSource, setPreviouslyUsedSource] = useState<string>("");
  const [
    previouslyUsedDevice,
    setPreviouslyUsedDevice,
  ] = useState<SelectOption | null>(null);
  const [responseData, setResponseData] = useState<MediaUploadResponse | null>(
    null
  );

  return (
    <>
      <LayoutBase>
        {responseData !== null ? (
          <Grid
            container
            alignItems="center"
            direction="column"
            justify="center"
            spacing={2}
          >
            <Grid item>
              <Typography variant="h4">{t("L'envoi a réussi")}</Typography>
            </Grid>
            <Grid
              item
              container
              alignItems="center"
              direction="row"
              justify="center"
              spacing={2}
            >
              {responseData.invalid_labels.length > 0 && (
                <Grid item>
                  <Typography variant="h5">
                    {t("Labels introuvables")}
                  </Typography>
                  <div>
                    {responseData.invalid_labels.map((invalidLabel) => (
                      <div key={invalidLabel.line}>
                        {t("Ligne ") +
                          invalidLabel.line +
                          ': "' +
                          invalidLabel.content +
                          '"'}
                      </div>
                    ))}
                  </div>
                </Grid>
              )}
              {responseData.invalid_lines.length > 0 && (
                <Grid item>
                  <Typography variant="h5">{t("Lignes invalides")}</Typography>
                  <div>
                    {responseData.invalid_lines.map((invalidLine) => (
                      <div key={invalidLine.line}>
                        {t("Ligne ") +
                          invalidLine.line +
                          ': "' +
                          invalidLine.content +
                          '"'}
                      </div>
                    ))}
                  </div>
                </Grid>
              )}
            </Grid>
            <Grid
              item
              container
              alignItems="center"
              direction="row"
              justify="center"
              spacing={5}
            >
              <Grid item>
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  onClick={() => router.push("/home")}
                >
                  {t("Retour à l'accueil")}
                </Button>
              </Grid>
              <Grid item>
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  onClick={() => setResponseData(null)}
                >
                  {t("Ajouter un enregistrement")}
                </Button>
              </Grid>
            </Grid>
          </Grid>
        ) : (
          <MediaUploadForm
            onResponse={setResponseData}
            onSourceChange={setPreviouslyUsedSource}
            onDeviceChange={setPreviouslyUsedDevice}
            defaultDevice={previouslyUsedDevice}
            defaultSource={previouslyUsedSource}
          />
        )}
      </LayoutBase>
    </>
  );
};

export default NewRecordingPage;
