import React, { useState } from "react";
import { theme } from "@/theme";
import {
  Button,
  Grid,
  makeStyles,
  TextField,
  LinearProgress,
  Typography,
  Tooltip,
} from "@material-ui/core";
import DeleteIcon from "../Icon/Delete";

const useStyles = makeStyles({
  filesListStyle: {
    display: "flex",
    flexDirection: "column",
    width: "100%",
  },
  listItemStyle: {
    display: "flex",
    alignItems: "center",
    width: "100%",
    lineHeight: "2rem",
    maxHeight: "2rem",
    fontSize: "1.2rem",
    margin: "5px 0 0 0",
    backgroundColor: theme.palette.secondary.light,
    color: "black",
    border: `1px solid ${theme.palette.primary.main}`,
    borderRadius: "3px",
    padding: "0 5px",
  },
  fileNameStyle: {
    margin: "0px",
    alignSelf: "start",
    whiteSpace: "nowrap",
    width: "90%",
    overflow: "hidden",
    fontSize: "0.9rem",
    textOverflow: "ellipsis",
  },
  deleteIconStyle: {
    width: "10%",
  },
});

interface FilesListProps {
  filesList: Array<File>;
  onFileDelete: (file: File) => void;
}

const FilesList: React.FC<FilesListProps> = (props) => {
  const classes = useStyles();

  return (
    <div
      className={classes.filesListStyle}
      onClick={(e) => {
        e.preventDefault();
        e.stopPropagation();
      }}
    >
      {props.filesList.map((file) => (
        <div className={classes.listItemStyle} key={file.name}>
          <Tooltip title={file.name} aria-label={file.name} placement="right">
            <div className={classes.fileNameStyle}>{`➤ ${file.name}`}</div>
          </Tooltip>
          <DeleteIcon
            className={classes.deleteIconStyle}
            onClick={() => props.onFileDelete(file)}
          />
        </div>
      ))}
    </div>
  );
};

export default FilesList;
