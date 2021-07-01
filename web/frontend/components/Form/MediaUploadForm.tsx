import React, { useState, useEffect } from "react";
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
import DatePicker, { registerLocale } from "react-datepicker";
import Dropzone, { FileWithPath } from "react-dropzone";
import "react-datepicker/dist/react-datepicker.css";
import frLocale from "date-fns/locale/fr";
import i18n from "i18next";
import axios from "axios";
import { SelectOption } from "@/models/utils";
import { MediaUploadResponse } from "@/models/media";
import { useRouter } from "next/router";
import MediaLinkIcon from "../Icon/MediaLink";
import UploadIcon from "../Icon/Upload";
import ToggleButton from "@material-ui/lab/ToggleButton";
import ToggleButtonGroup from "@material-ui/lab/ToggleButtonGroup";
import InputMask from "react-input-mask";
import DynamicSelect from "@/components/Form/DynamicSelect";
import useSWR from "swr";
import { Alert } from "@material-ui/lab";
import FilesList from "./FilesList";

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
  formSection: {
    backgroundColor: "#163751",
    margin: "20px 0px",
    padding: "20px",
    border: "1px solid white",
    borderRadius: "4px",
  },
  warningMessage: {
    margin: "0 0 20px 0",
    width: "100%",
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
    borderWidth: "2px",
    borderRadius: "2px",
    borderColor: "#163751",
    borderStyle: "dashed",
    backgroundColor: "#fafafa",
    color: "#bdbdbd",
    outline: "none",
    transition: "border .24s ease-in-out",
    padding: "5px 10px",
  },
  buttonGroupLabel: {
    textTransform: "initial",
    margin: "3px 10px",
  },
  mediaFromURLForm: {
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
  },
  alertBox: {
    marginTop: 15,
    alignItems: "center",
    whiteSpace: "pre-line",
  },
});

const parseDurationInputIntoSeconds = (durationString: string) => {
  const hours = parseInt(durationString.slice(0, 2).replace(/\D/g, "")) || 0;
  const min = parseInt(durationString.slice(4, 6).replace(/\D/g, "")) || 0;
  const sec = parseInt(durationString.slice(8, 10).replace(/\D/g, "")) || 0;

  if (min > 59 || sec > 59) return -1;

  return hours * 3600 + min * 60 + sec;
};

interface MediaUploadFormProps {
  onResponse(response: MediaUploadResponse): void;
  onDeviceChange(option: SelectOption | null): void;
  onSiteChange(option: SelectOption | null): void;
  onSourceChange(source: string): void;
  defaultSource?: string;
  defaultDevice?: SelectOption;
  defaultSite?: SelectOption;
}

const MediaUploadForm: React.FC<MediaUploadFormProps> = (props) => {
  const classes = useStyles();
  const { t } = useTranslation();
  const router = useRouter();
  const { accessToken } = useAuth();

  // Standard label search by API call with timeout
  const requestTimeoutMilliseconds = 1000;
  const [
    labelRequestTimeout,
    setLabelRequestTimeout,
  ] = useState<null | ReturnType<typeof setTimeout>>(null);

  const [deviceRequestParameter, setDeviceRequestParameter] = useState<string>(
    "?model_name="
  );
  const setDeviceInput = (input) => {
    if (labelRequestTimeout !== null) {
      clearTimeout(labelRequestTimeout);
      setLabelRequestTimeout(null);
    }
    setLabelRequestTimeout(
      setTimeout(() => {
        setDeviceRequestParameter(
          "?model_name=" + (input.length > 3 ? input : "")
        );
        setLabelRequestTimeout(null);
      }, requestTimeoutMilliseconds)
    );
  };
  const { data: devicesList } = useSWR([
    `/devices/${deviceRequestParameter}`,
    accessToken,
  ]);

  // Other properties
  const [progressPercents, setProgressPercents] = useState<Array<number>>([]);
  const [progressUpdate, setProgressUpdate] = useState<{
    index: number;
    value: number;
  } | null>(null);
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
  const [siteOption, _setSiteOption] = useState<SelectOption | null>(
    props.defaultSite || null
  );
  const setSiteOption = (option: SelectOption | null) => {
    if (option?.value === 0) {
      option = null;
    }
    _setSiteOption(option);
    props.onSiteChange(option);
  };

  const setFileSource = (source: string) => {
    _setFileSource(source);
    props.onSourceChange(source);
  };

  const [startDate, setStartDate] = useState<Date | null>(null);
  const [createMediaMode, setCreateMediaMode] = useState<string>(
    "MEDIA_UPLOAD"
  );
  const [audioFiles, setAudioFiles] = useState<Array<File>>([]);
  const [audioFileUrl, setAudioFileUrl] = useState<string>("");
  const [audioFileDuration, setAudioFileDuration] = useState<string | null>("");
  const [annotationFiles, setAnnotationFiles] = useState<Array<File>>([]);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const locales = { fr: frLocale };
  let datePickerLanguage = "en";
  if (locales[i18n.language]) {
    datePickerLanguage = i18n.language;
    registerLocale(i18n.language, locales[i18n.language]);
  }

  const onAudioDrop = (acceptedFiles) => {
    const updatedAudioFiles = audioFiles.slice();
    const audioFilesPaths = audioFiles.map((file: FileWithPath) => file.path);
    acceptedFiles.forEach((file: FileWithPath) => {
      if (!audioFilesPaths.includes(file.path)) {
        updatedAudioFiles.push(file);
        audioFilesPaths.push(file.path);
      }
    });
    setAudioFiles(updatedAudioFiles);
  };
  const onAnnotationsDrop = (acceptedFiles) => {
    const updatedAnnotationFiles = annotationFiles.slice();
    const annotationFilesPaths = annotationFiles.map(
      (file) => (file as any).path
    );
    acceptedFiles.forEach((file: FileWithPath) => {
      if (!annotationFilesPaths.includes(file.path)) {
        updatedAnnotationFiles.push(file);
        annotationFilesPaths.push(file.path);
      }
    });
    setAnnotationFiles(updatedAnnotationFiles);
  };

  useEffect(() => {
    // some code to fetch data
    if (progressUpdate !== null)
      updateProgressPercents(progressUpdate.index, progressUpdate.value);
  }, [progressUpdate]);

  const updateProgressPercents = (index: number, newValue: number) => {
    const updatedProgress = progressPercents.slice();
    updatedProgress[index] = newValue;
    setProgressPercents(updatedProgress);
  };

  const handleCreateMediaModeChange = (e, nextMode) => {
    if (nextMode !== null) {
      setCreateMediaMode(nextMode);
    }
    if (nextMode === "MEDIA_URL") {
      if (annotationFiles.length > 1) {
        setAnnotationFiles(annotationFiles.slice(0, 1));
      }
      if (audioFiles.length > 1) {
        setAudioFiles(audioFiles.slice(0, 1));
      }
    }
  };

  const handleCreateMedia = async (e) => {
    e.preventDefault();
    try {
      // Validate that annotation files are text files
      if (
        annotationFiles.length === 0 ||
        !annotationFiles
          .map((file) => file.type.startsWith("text"))
          .reduce((accumulator, currentValue) => accumulator && currentValue)
      ) {
        return alert(t("chooseTextFile"));
      }

      // Validate that all annotation files are audio files
      if (createMediaMode === "MEDIA_UPLOAD") {
        if (
          audioFiles.length === 0 ||
          !audioFiles
            .map((file) => file.type.startsWith("audio"))
            .reduce((accumulator, currentValue) => accumulator && currentValue)
        ) {
          return alert(t("chooseAudioFile"));
        }
      } else if (createMediaMode === "MEDIA_URL") {
        const duration = parseDurationInputIntoSeconds(audioFileDuration);
        if (duration <= 0) {
          return alert(t("impossibleAudioDuration"));
        }
        if (duration >= 24 * 60 * 60) {
          // duration greater than 24 hours
          return alert(t("maximumAudioDuration"));
        }
      }

      // TODO: Validate that sites is set
      // if (siteOption !== null && typeof siteOption.value !== "number") {
      //   return alert(t("chooseValidSite"));
      // }

      // IF "single recording upload", validate context info
      if (audioFiles.length <= 1 && annotationFiles.length === 1) {
        if (startDate === null || typeof startDate.getMonth !== "function") {
          return alert(t("chooseBeginDate"));
        }

        if (deviceOption === null || typeof deviceOption.value !== "number") {
          return alert(t("chooseRecorder"));
        }
      }

      // IF "multiple recordings upload", validate audio-text files coupling
      if (audioFiles.length > 1 || annotationFiles.length > 1) {
        const audioAndAnnotationCouples = [];
        audioFiles.forEach((audioFile: FileWithPath) => {
          annotationFiles.forEach((annotationFile: FileWithPath) => {
            const audioName = audioFile.path.replace(/\.[^/.]+$/, "");
            const annotationName = annotationFile.path.replace(/\.[^/.]+$/, "");
            if (audioName === annotationName) {
              audioAndAnnotationCouples.push(audioName);
            }
          });
        });
        const audioMissingAnnotation = audioFiles
          .filter(
            (file: FileWithPath) =>
              !audioAndAnnotationCouples.includes(
                file.path.replace(/\.[^/.]+$/, "")
              )
          )
          .map((file: FileWithPath) => file.path);
        const annotationsMissingAudio = annotationFiles
          .filter(
            (file: FileWithPath) =>
              !audioAndAnnotationCouples.includes(
                file.path.replace(/\.[^/.]+$/, "")
              )
          )
          .map((file: FileWithPath) => file.path);
        if (
          audioMissingAnnotation.length > 0 ||
          annotationsMissingAudio.length > 0
        ) {
          let alertMsg = `${t("recordingFilesMissmatch")}\n\n`;
          if (audioMissingAnnotation.length > 0) {
            alertMsg += `${t(
              "recordingFilesAudioMissingAnnotation"
            )}:\n- ${audioMissingAnnotation.join("\n- ")}\n\n`;
          }
          if (annotationsMissingAudio.length > 0) {
            alertMsg += `${t(
              "recordingFilesAnnotationsMissingAudio"
            )}:\n- ${annotationsMissingAudio.join("\n- ")}\n\n`;
          }
          return alert(alertMsg);
        }
      }

      // Build data forms to be sent to the backend to create recording
      const uploadForms = [];
      if (annotationFiles.length === 1) {
        const formData = new FormData();
        formData.append("file_source", fileSource);
        formData.append("begin_date", startDate.toISOString());
        formData.append("device_id", deviceOption?.value.toString());
        if (siteOption !== null) {
          formData.append("site_id", siteOption.value.toString());
        }
        if (createMediaMode === "MEDIA_URL") {
          formData.append("audio_url", audioFileUrl);
          formData.append(
            "audio_duration",
            parseDurationInputIntoSeconds(audioFileDuration).toString()
          );
        } else {
          formData.append("audio_file", audioFiles[0]);
        }
        formData.append("annotations", annotationFiles[0]);
        uploadForms.push(formData);
      } else {
        audioFiles.forEach((audioFile: FileWithPath, index) => {
          const formData = new FormData();
          formData.append("file_source", `${fileSource}-${index}`);
          formData.append("audio_file", audioFile);
          formData.append(
            "annotations",
            annotationFiles.find(
              (file: FileWithPath) =>
                file.path.replace(/\.[^/.]+$/, "") ===
                audioFile.path.replace(/\.[^/.]+$/, "")
            )
          );
          uploadForms.push(formData);
        });
      }

      // Call backend for each data form
      const apiRoute = `${process.env.API_URL}/mediae/upload`;
      const headers = {
        "Content-Type": "multipart/form-data",
        Authorization: `Bearer ${accessToken}`,
      };
      const uploadRequests = [];
      setProgressPercents(new Array(uploadForms.length).fill(0));
      uploadForms.forEach((formData, index) => {
        uploadRequests.push(
          axios.post(apiRoute, formData, {
            headers: headers,
            onUploadProgress: async function (progressEvent) {
              const percentCompleted = Math.round(
                (progressEvent.loaded * 100) / progressEvent.total
              );
              setProgressUpdate({ index, value: percentCompleted });
            },
          })
        );
      });

      axios.all(uploadRequests).then(
        axios.spread((...responses) => {
          const aggregateMediaLabelData = {
            invalid_lines: [],
            mediae: [],
            mediaelabels: [],
          };
          let status = 200;
          const errorDetails = [];
          responses.forEach((response, index) => {
            aggregateMediaLabelData.invalid_lines.push(
              ...response.data.invalid_lines
            );
            aggregateMediaLabelData.mediae.push(response.data.media);
            aggregateMediaLabelData.mediaelabels.push(
              ...response.data.medialabels
            );
            if (response.status !== 200) {
              status = response.status;
              if (response.data.detail) {
                errorDetails.push(response.data.detail);
              }
            }
          });
          if (status === 200) {
            props.onResponse(aggregateMediaLabelData);
          } else {
            setUploadError(
              errorDetails.length > 0
                ? errorDetails.map((detail) => t(detail[0].type)).join("\n")
                : t("unknown_error")
            );
          }
        })
      );
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
      {progressPercents.length > 0 &&
      progressPercents.reduce((a, b) => a + b) > 0 ? (
        uploadError ? (
          <Grid
            container
            alignItems="center"
            direction="column"
            justify="center"
            spacing={2}
          >
            <Grid item>
              <Typography variant="h4">{t("errorDuringUpload")}</Typography>
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
                    setProgressPercents(
                      new Array(annotationFiles.length).fill(0)
                    );
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
              <LinearProgress
                variant="determinate"
                value={
                  Object.values(progressPercents).reduce((a, b) => a + b) /
                  Object.values(progressPercents).length
                }
              />
              {Math.round(
                Object.values(progressPercents).reduce((a, b) => a + b) /
                  Object.values(progressPercents).length
              )}
              %
            </div>
          </div>
        )
      ) : (
        <form onSubmit={handleCreateMedia} autoComplete="off">
          <Alert severity="info" className={classes.alertBox}>
            <Typography variant="h5">
              {t("Méthodologie d'ajout de fichiers")}
            </Typography>
            <div>
              Avant de déposer vos fichiers veuillez vous assurez vous que vous
              avez bien suivi les procédures d'annotations proposées:&nbsp;
              <a
                target="_blank"
                href="https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/blob/master/docs/Audiofile_annotation_methods_NBM.pdf"
              >
                https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/blob/master/docs/Audiofile_annotation_methods_NBM.pdf
              </a>
              <br />
              Ensuite, renseigner la source de votre fichier son (source
              personnelle, enregistrement d'un.e ami.e, source externe (site
              web), etc.)
              <br />
              Sélectionner un enregistreur présent dans la liste et une date de
              début d'enregistrement.
              <br />
              Déposer le fichier son (en .wav) et le fichier d'annotation
              associé (.txt).
              <br />
              <br />
              NB : Les fichiers envoyés seront stockés sous licence libre:&nbsp;
              <a
                target="_blank"
                href="https://creativecommons.org/licenses/by/4.0/deed.fr"
              >
                https://creativecommons.org/licenses/by/4.0/deed.fr
              </a>
              <br />
              Ces fichiers pourront être utilisés par tous. Dans le cadre du
              projet NBM ils servent à entrainer une intelligence artifcielle.
            </div>
          </Alert>
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
              className={classes.formSection}
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
                <DynamicSelect
                  columnName="model_name"
                  endpoint="/devices/"
                  placeholder={t("recorderModel")}
                  defaultValue={deviceOption}
                  onChange={setDeviceOption}
                />
              </Grid>
              <Grid item xs={12} sm={6} className={classes.formItem}>
                <DynamicSelect
                  columnName="name"
                  endpoint="/sites/"
                  optionalText={t("noAssociatedSite")}
                  placeholder={t("associatedSite")}
                  defaultValue={siteOption}
                  onChange={setSiteOption}
                />
              </Grid>
              <Grid item xs className={classes.formItem}>
                <label>{t("recordingBeginDate")}</label>
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
              className={classes.formSection}
            >
              <Grid item xs={12}>
                <Typography variant="h4">{t("files")}</Typography>
              </Grid>
              <Grid item xs={12} className={classes.formItem}>
                <ToggleButtonGroup
                  size="small"
                  orientation="horizontal"
                  value={createMediaMode}
                  exclusive
                  onChange={handleCreateMediaModeChange}
                >
                  <ToggleButton value="MEDIA_UPLOAD" aria-label="MEDIA_UPLOAD">
                    <UploadIcon />
                    <label className={classes.buttonGroupLabel}>
                      {t("addMediaFromComputer")}
                    </label>
                  </ToggleButton>
                  <ToggleButton value="MEDIA_URL" aria-label="MEDIA_URL">
                    <MediaLinkIcon />
                    <label className={classes.buttonGroupLabel}>
                      {t("addMediaFromInternet")}
                    </label>
                  </ToggleButton>
                </ToggleButtonGroup>
              </Grid>
              <Grid
                item
                xs={12}
                sm={6}
                className={classes.formItem}
                style={{ alignSelf: "stretch" }}
              >
                {createMediaMode === "MEDIA_UPLOAD" ? (
                  <Dropzone
                    accept={["audio/*"]}
                    onDrop={onAudioDrop}
                    multiple={true}
                  >
                    {({ getRootProps, getInputProps }) => (
                      <div {...getRootProps()} className={classes.dropZone}>
                        <input {...getInputProps()} />
                        <p>{t("clicOrDropYouAudioFile")}</p>
                        <FilesList
                          filesList={audioFiles}
                          onFileDelete={(fileToDelete: File) => {
                            setAudioFiles((prev) =>
                              prev.filter(
                                (file) =>
                                  (file as any).path !==
                                  (fileToDelete as any).path
                              )
                            );
                          }}
                        />
                      </div>
                    )}
                  </Dropzone>
                ) : (
                  <div className={classes.mediaFromURLForm}>
                    <TextField
                      color="secondary"
                      variant="outlined"
                      margin="none"
                      required
                      fullWidth
                      value={audioFileUrl}
                      id="new-media-url"
                      label={t("mediaUrl")}
                      name="new-media-url"
                      onChange={(event) => setAudioFileUrl(event.target.value)}
                      autoFocus
                    />

                    <InputMask
                      mask="99h 99m 99s"
                      value={audioFileDuration}
                      maskChar="_"
                      onChange={(event) =>
                        setAudioFileDuration(event.target.value)
                      }
                    >
                      {() => (
                        <TextField
                          color="secondary"
                          variant="outlined"
                          margin="dense"
                          required
                          fullWidth
                          value={audioFileDuration}
                          id="new-media-duration"
                          label={t("audioFileDuration")}
                          name="new-media-duration"
                        />
                      )}
                    </InputMask>
                  </div>
                )}
              </Grid>
              <Grid
                item
                xs={12}
                sm={6}
                className={classes.formItem}
                style={{ alignSelf: "stretch" }}
              >
                <Dropzone
                  accept={["text/plain"]}
                  onDrop={onAnnotationsDrop}
                  multiple={createMediaMode === "MEDIA_UPLOAD"}
                >
                  {({ getRootProps, getInputProps }) => (
                    <div {...getRootProps()} className={classes.dropZone}>
                      <input {...getInputProps()} />
                      <p>{t("clicOrDropYourTextFile")}</p>
                      <FilesList
                        filesList={annotationFiles}
                        onFileDelete={(fileToDelete: File) => {
                          setAnnotationFiles((prev) =>
                            prev.filter(
                              (file) =>
                                (file as any).path !==
                                (fileToDelete as any).path
                            )
                          );
                        }}
                      />
                    </div>
                  )}
                </Dropzone>
              </Grid>
            </Grid>

            {audioFiles.length > 1 && (
              <Alert severity="warning" className={classes.warningMessage}>
                {t("warningMultipleUploads")}
              </Alert>
            )}
            <Grid item xs>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                className={classes.bottomButton}
              >
                {t("sendRecordings")}
              </Button>
            </Grid>
          </Grid>
        </form>
      )}
    </div>
  );
};

export default MediaUploadForm;
