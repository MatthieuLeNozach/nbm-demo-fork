import LayoutBase from "@/components/layout/base";
import React, { useState } from "react";
import MediaUploadForm from "@/components/MediaUploadForm";
import Button from "@material-ui/core/Button";
import { useRouter } from "next/router";
import { SelectOption } from "@/models/utils";
import { MediaUploadResponse } from "@/models/media";
import { useTranslation } from "react-i18next";
import { Grid, makeStyles, Typography } from "@material-ui/core";
import useSWR from "swr";
import { useAuth } from "@/components/Providers/AuthProvider";
import Select from "react-select";
import axios from "axios";
import { MediaLabel } from "@/models/medialabel";

const useStyles = makeStyles({
  section: {
    backgroundColor: "#163751",
    border: "1px solid white",
    borderRadius: "4px",
    margin: "10px",
  },
  marginLeftAuto: {
    marginLeft: "auto",
  },
  tableLine: {
    borderTop: "1px solid grey",
    marginTop: "10px",
  },
  tableColumn: {
    flex: 1,
    minWidth: "185px",
  },
  bottomButtons: {
    margin: 0,
  },
});

const customSelectStyles = {
  option: (provided) => ({
    ...provided,
    color: "black",
  }),
  container: (provided) => {
    return {
      ...provided,
      minWidth: "300px",
    };
  },
  control: (provided) => {
    return {
      ...provided,
      backgroundColor: "inherit",
      border: "1px solid rgba(0, 0, 0, 0.23)",
    };
  },
  valueContainer: (provided) => {
    return { ...provided, padding: 13 };
  },
  singleValue: (provided) => {
    return { ...provided, color: "white" };
  },
  input: (provided) => {
    return { ...provided, color: "white" };
  },
  placeholder: (provided) => {
    return { ...provided, color: "white" };
  },
};

const NewRecordingPage = () => {
  const classes = useStyles();
  const router = useRouter();
  const { t } = useTranslation();
  const { accessToken } = useAuth();

  // Standard label search by API call with timeout
  const requestTimeoutMilliseconds = 1000;
  const [
    labelRequestTimeout,
    setLabelRequestTimeout,
  ] = useState<null | ReturnType<typeof setTimeout>>(null);
  const setLabelInput = (input) => {
    if (labelRequestTimeout !== null) {
      clearTimeout(labelRequestTimeout);
      setLabelRequestTimeout(null);
    }
    setLabelRequestTimeout(
      setTimeout(() => {
        setLabelRequestParameter(input.length > 3 ? "?name=" + input : "");
        setLabelRequestTimeout(null);
      }, requestTimeoutMilliseconds)
    );
  };
  const [labelRequestParameter, setLabelRequestParameter] = useState<string>(
    ""
  );
  const { data: labelsList } = useSWR([
    `/standardlabels/${labelRequestParameter}`,
    accessToken,
  ]);

  // Others properties
  const [previouslyUsedSource, setPreviouslyUsedSource] = useState<string>("");
  const [
    previouslyUsedDevice,
    setPreviouslyUsedDevice,
  ] = useState<SelectOption | null>(null);
  const [invalidMediaLabels, setInvalidMediaLabels] = useState<
    Array<MediaLabel>
  >([]);
  const setLabelOption = (labelOption: SelectOption, labelId: number) => {
    updatedMediaLabels[labelId] = labelOption;
    setUpdatedMediaLabels(updatedMediaLabels);
  };

  const [responseData, _setResponseData] = useState<MediaUploadResponse | null>(
    null
  );
  const setResponseData = (response) => {
    _setResponseData(response);

    if (!response) {
      return;
    }

    setInvalidMediaLabels(
      response.medialabels.filter(
        (medialabel) => medialabel.invalid_label_text !== null
      )
    );
  };

  const [updatedMediaLabels, setUpdatedMediaLabels] = useState<{
    [k: number]: SelectOption;
  }>({});
  const updateMediaLabels = () => {
    const promises = [];
    for (const [mediaLabelId, option] of Object.entries(updatedMediaLabels)) {
      promises.push(
        axios.put(
          `${process.env.API_URL}/medialabels/${mediaLabelId}`,
          { label_id: option.value.toString(), invalid_label_text: null },
          {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: `Bearer ${accessToken}`,
            },
          }
        )
      );
    }
    Promise.all(promises).then(() => {
      setInvalidMediaLabels(
        invalidMediaLabels.filter(
          (medialabel) => !updatedMediaLabels[medialabel.id]
        )
      );
      setUpdatedMediaLabels({});
    });
  };

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
              <Typography variant="h4">{t("successfulSending")}</Typography>
              <div>
                {t("annotationAdded", {
                  count: responseData.medialabels.length,
                })}
              </div>
            </Grid>
            <Grid
              item
              container
              alignItems="flex-start"
              direction="row"
              justify="center"
              spacing={2}
            >
              {invalidMediaLabels.length > 0 && (
                <Grid item className={classes.section}>
                  <Typography variant="h5">
                    {t("labelNotFound", { count: invalidMediaLabels.length })}
                  </Typography>
                  <Typography variant="h6">
                    {t("updateLabelsNowOrLater")}
                  </Typography>
                  {invalidMediaLabels.map((medialabel) => (
                    <Grid
                      container
                      alignItems="center"
                      direction="row"
                      justify="flex-start"
                      spacing={2}
                      key={medialabel.begin_time}
                      className={classes.tableLine}
                    >
                      <Grid item className={classes.tableColumn}>
                        {t("beginTime") + " " + medialabel.begin_time}:{" "}
                      </Grid>
                      <Grid item className={classes.tableColumn}>
                        <b> {medialabel.invalid_label_text}</b>
                      </Grid>
                      <Grid item className={classes.marginLeftAuto}>
                        <Select
                          placeholder={t("standardLabel")}
                          styles={customSelectStyles}
                          instanceId={"label-select" + medialabel.id}
                          onChange={(e) => setLabelOption(e, medialabel.id)}
                          onInputChange={setLabelInput}
                          options={
                            Array.isArray(labelsList)
                              ? labelsList.map((label) => ({
                                  value: label.id,
                                  label: label.name,
                                }))
                              : []
                          }
                        />
                      </Grid>
                    </Grid>
                  ))}
                </Grid>
              )}
              {responseData.invalid_lines.length > 0 && (
                <Grid item className={classes.section}>
                  <Typography variant="h5">{t("invalidLines")}</Typography>
                  {responseData.invalid_lines.map((invalidLine) => (
                    <Grid
                      container
                      alignItems="center"
                      direction="row"
                      justify="flex-start"
                      spacing={2}
                      key={invalidLine.line}
                      className={classes.tableLine}
                    >
                      <Grid item>
                        {t("line") + " " + invalidLine.line + ":"}
                      </Grid>
                      <Grid item>{invalidLine.content}</Grid>
                      {invalidLine.detail && (
                        <Grid item className={classes.marginLeftAuto}>
                          <b>{t(invalidLine.detail)}</b>
                        </Grid>
                      )}
                    </Grid>
                  ))}
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
              className={classes.bottomButtons}
            >
              <Grid item>
                <Button
                  type="button"
                  variant="contained"
                  color="primary"
                  onClick={() => router.push("/home")}
                >
                  {t("backToHome")}
                </Button>
              </Grid>
              <Grid item>
                <Button
                  type="button"
                  variant="contained"
                  color="primary"
                  onClick={() => setResponseData(null)}
                >
                  {t("addRecording")}
                </Button>
              </Grid>
              {invalidMediaLabels.length > 0 && (
                <Grid item>
                  <Button
                    type="button"
                    variant="contained"
                    color="primary"
                    onClick={() => updateMediaLabels()}
                  >
                    {t("updateMediaLabels")}
                  </Button>
                </Grid>
              )}
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
