import LayoutBase from "@/components/layout/base";
import { theme } from "@/theme";
import { Button, makeStyles } from "@material-ui/core";
import { Container } from "next/app";

const useStyles = makeStyles({
    toolbar: {
      backgroundColor: theme.palette.primary.main,
      height: 50,
    },
  });

const HomePage = ({ children }) => {

    const classes = useStyles();

    return (
      <>
        <LayoutBase>
            <Button name="Explore recordings" className={classes.toolbar}/>
            <Button name="My recordings" className={classes.toolbar}/>
            <Button name="Manage my sites" className={classes.toolbar}/>
            <Button name="Submit new recording" className={classes.toolbar}/>
        </LayoutBase>
      </>
    );
  };
  
  export default HomePage;