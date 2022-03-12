import { FC, ReactElement } from "react";
import { Grid, makeStyles } from "@material-ui/core";
import { useRouter } from "next/router";

export interface DashboardItemProps {
  label: string;
  total: number;
  icon: ReactElement;
  href?: string;
}

const useStyles = makeStyles((theme) => ({
  box: {
    minWidth: "6.5rem",
    cursor: (props: DashboardItemProps) => (props.href ? "pointer" : "auto"),
  },

  [theme.breakpoints.up("md")]: {
    item: {
      borderRight: "1px solid #ddd",

      "&:hover": {
        background: (props: DashboardItemProps) =>
          props.href ? "#0721363b" : "transparent",
        transition: ".3s background",
      },
    },
  },
}));

const DashboardItem: FC<DashboardItemProps> = ({
  label,
  total,
  icon,
  href,
}) => {
  const classes = useStyles({ label, total, icon, href });
  const router = useRouter();

  const handleGoToPage = () => {
    if (href) {
      router.push(href);
    }
  };

  return (
    <Grid
      className={classes.item}
      item
      key={`${label}`}
      onClick={handleGoToPage}
    >
      <Grid
        className={classes.box}
        container
        direction="column"
        alignItems="center"
      >
        <Grid item>{icon}</Grid>
        <Grid item> {total || "N/A"} </Grid>
        <Grid item>{label} </Grid>
      </Grid>
    </Grid>
  );
};

export default DashboardItem;
