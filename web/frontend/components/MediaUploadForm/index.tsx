import React, { useState } from "react";
import { theme } from "@/theme";
import {
  Button,
  Grid,
  makeStyles,
  TextField,
  LinearProgress,
  Typography,
} from "@material-ui/core";
import { useTranslation } from "react-i18next";
import { useAuth } from "@/components/Providers/AuthProvider";
import useSWR from "swr";
import DatePicker, { registerLocale } from "react-datepicker";
import Dropzone from "react-dropzone";
import "react-datepicker/dist/react-datepicker.css";
import frLocale from "date-fns/locale/fr";
import Select from "react-select";
import i18n from "i18next";
import axios from "axios";
import { SelectOption } from "@/models/utils";
import { MediaUploadResponse } from "@/models/media";
import { useRouter } from "next/router";

const useStyles = makeStyles({
  bottomButton: {
    fontSize: "15px",
    lineHeight: "26px",
    color: "#FFFFFF",
    backgroundColor: theme.palette.primary.main,
    margin: "0 25px 25px",
    width: "243px",
    minHeight: "68px",
    textAlign: "center",
  },
  globalGrid: {
    maxWidth: "800px",
    margin: "auto",
  },
  fromSection: {
    backgroundColor: "#163751",
    margin: "20px 0px",
    padding: "20px",
    border: "1px solid white",
    borderRadius: "4px",
  },
  formItem: {
    margin: "10px 0",
    padding: "0 10px",
  },
  deviceSelect: {
    width: "100%",
    marginTop: "15px",
  },
  datepicker: {
    width: "100%",
    padding: "19px",
    backgroundColor: "inherit",
    position: "relative",
    top: "-5px",
    border: "1px solid rgba(0, 0, 0, 0.23)",
    borderRadius: "4px",
    color: "white",
  },
  datePickerContainer: {
    width: "100%",
    display: "block",
  },
  dropZone: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    padding: "20px",
    borderWidth: "2px",
    borderRadius: "2px",
    borderColor: "#163751",
    borderStyle: "dashed",
    backgroundColor: "#fafafa",
    color: "#bdbdbd",
    outline: "none",
    transition: "border .24s ease-in-out",
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
      position: "relative",
      top: "12px",
      marginBottom: "20px",
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

interface MediaUploadFormProps {
  onResponse(response: MediaUploadResponse): void;
  onDeviceChange(option: SelectOption | null): void;
  onSourceChange(source: string): void;
  defaultSource?: string;
  defaultDevice?: SelectOption;
}

const MediaUploadForm: React.FC<MediaUploadFormProps> = (props) => {
  const classes = useStyles();
  const { t } = useTranslation();
  const router = useRouter();
  const { accessToken } = useAuth();
  const [progressPercent, setProgressPercent] = useState<number>(0);
  const [fileSource, _setFileSource] = useState<string>(
    props.defaultSource || ""
  );
  const [deviceOption, _setDeviceOption] = useState<SelectOption | null>(
    props.defaultDevice || null
  );

  const setDeviceOption = (option: SelectOption | null) => {
    _setDeviceOption(option);
    props.onDeviceChange(option);
  };

  const setFileSource = (source: string) => {
    _setFileSource(source);
    props.onSourceChange(source);
  };

  const [deviceInput, setDeviceInput] = useState<string>("");
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [annotationsFile, setAnnotationsFile] = useState<File | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const locales = { fr: frLocale };
  let datePickerLanguage = "en";
  if (locales[i18n.language]) {
    datePickerLanguage = i18n.language;
    registerLocale(i18n.language, locales[i18n.language]);
  }

  const { data: devicesList } = useSWR([
    `/devices/${deviceInput.length ? "?model_name=" + deviceInput : ""}`,
    accessToken,
  ]);

  const onAudioDrop = (acceptedFiles) => {
    setAudioFile(acceptedFiles[0]);
  };
  const onAnnotationsDrop = (acceptedFiles) => {
    setAnnotationsFile(acceptedFiles[0]);
  };

  const handleCreateMedia = async (e) => {
    e.preventDefault();
    try {
      if (startDate === null || typeof startDate.getMonth !== "function") {
        return alert(
          t("chooseBeginDate")
        );
      }

      if (deviceOption === null || typeof deviceOption.value !== "number") {
        return alert(t("chooseRecorder"));
      }

      if (!audioFile || !audioFile.type.startsWith("audio")) {
        return alert(t("chooseAudioFile"));
      }
      if (!annotationsFile || !annotationsFile.type.startsWith("text")) {
        return alert(
          t("chooseTextFile")
        );
      }
      const formData = new FormData();
      formData.append("audio", audioFile);
      formData.append("annotations", annotationsFile);
      formData.append("begin_date", startDate.toISOString());
      formData.append("device_id", deviceOption?.value.toString());
      formData.append("file_source", fileSource);
      const { data, status } = await axios.post(
        `${process.env.API_URL}/mediae/upload`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${accessToken}`,
          },
          onUploadProgress: function (progressEvent) {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setProgressPercent(percentCompleted);
          },
        }
      );
      if (status === 200) {
        props.onResponse(data);
      } else {
        setUploadError(
          Array.isArray(data?.detail)
            ? t(data.detail[0].type)
            : t("unknown_error")
        );
      }
    } catch (error) {
      setUploadError(
        Array.isArray(error.response?.data?.detail)
          ? t(error.response.data.detail[0].type)
          : t("unknown_error")
      );
    }
  };

  return (
    <div>
      {progressPercent > 0 ? (
        uploadError ? (
          <Grid
            container
            alignItems="center"
            direction="column"
            justify="center"
            spacing={2}
          >
            <Grid item>
              <Typography variant="h4">
                {t("errorDuringUpload")}
              </Typography>
              <Typography variant="h5">{" (" + uploadError + ")"}</Typography>
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
                  variant="contained"
                  color="primary"
                  onClick={() => {
                    setProgressPercent(0);
                    setUploadError(null);
                  }}
                >
                  {t("retry")}
                </Button>
              </Grid>
              <Grid item>
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  onClick={() => router.push("/home")}
                >
                  {t("backToHome")}
                </Button>
              </Grid>
            </Grid>
          </Grid>
        ) : (
          <div>
            <Typography variant="h4">{t("loading")}</Typography>
            <div>
              <LinearProgress variant="determinate" value={progressPercent} />
              {progressPercent}%
            </div>
          </div>
        )
      ) : (
        <form onSubmit={handleCreateMedia}>
          <Grid
            container
            direction="column"
            justify="flex-start"
            alignItems="center"
            className={classes.globalGrid}
          >
            <Grid
              item
              container
              direction="row"
              alignItems="flex-start"
              className={classes.fromSection}
            >
              <Grid item xs={12}>
                <Typography variant="h4">{t("context")}</Typography>
              </Grid>
              <Grid item xs={12} className={classes.formItem}>
                <TextField
                  color="secondary"
                  variant="outlined"
                  margin="normal"
                  required
                  fullWidth
                  value={fileSource}
                  id="file-source"
                  label={t("fileSource")}
                  name="file-source"
                  onChange={(event) => setFileSource(event.target.value)}
                  autoFocus
                />
              </Grid>
              <Grid item xs={12} sm={6} className={classes.formItem}>
                <Select
                  placeholder={t("recorderModel")}
                  styles={customSelectStyles}
                  instanceId="device-select"
                  defaultValue={deviceOption}
                  onChange={setDeviceOption}
                  onInputChange={setDeviceInput}
                  options={
                    Array.isArray(devicesList)
                      ? devicesList.map((device) => ({
                          value: device.id,
                          label: device.model_name,
                        }))
                      : []
                  }
                />
              </Grid>
              <Grid item xs className={classes.formItem}>
                <label>{t("recordingDate")}</label>
                <DatePicker
                  selected={startDate}
                  onChange={(date) => setStartDate(date)}
                  maxDate={new Date()}
                  showTimeSelect
                  dateFormat="Pp"
                  timeIntervals="5"
                  locale={datePickerLanguage}
                  className={classes.datepicker}
                  wrapperClassName={classes.datePickerContainer}
                />
              </Grid>
            </Grid>
            <Grid
              item
              container
              direction="row"
              justify="flex-start"
              alignItems="center"
              className={classes.fromSection}
            >
              <Grid item xs={12}>
                <Typography variant="h4">{t("files")}</Typography>
              </Grid>
              <Grid item xs={12} sm className={classes.formItem}>
                <Dropzone
                  accept={["audio/*"]}
                  onDrop={onAudioDrop}
                  multiple={false}
                >
                  {({ getRootProps, getInputProps }) => (
                    <div {...getRootProps()} className={classes.dropZone}>
                      <input {...getInputProps()} />
                      <p>{t("clicOrDropYouAudioFile")}</p>
                      {audioFile && (
                        <p>
                          {t("selectedFiles")} {audioFile.name}
                        </p>
                      )}
                    </div>
                  )}
                </Dropzone>
              </Grid>
              <Grid item xs={12} sm className={classes.formItem}>
                <Dropzone
                  accept={["text/plain"]}
                  onDrop={onAnnotationsDrop}
                  multiple={false}
                >
                  {({ getRootProps, getInputProps }) => (
                    <div {...getRootProps()} className={classes.dropZone}>
                      <input {...getInputProps()} />
                      <p>
                        {t(
                          "clicOrDropYourTextFile"
                        )}
                      </p>
                      {annotationsFile && (
                        <p>
                          {t("selectedFiles")} {annotationsFile.name}
                        </p>
                      )}
                    </div>
                  )}
                </Dropzone>
              </Grid>
            </Grid>
            <Grid item xs>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                className={classes.bottomButton}
              >
                {t("add")}
              </Button>
            </Grid>
          </Grid>
        </form>
      )}
    </div>
  );
};

export default MediaUploadForm;
