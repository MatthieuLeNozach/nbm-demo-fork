import { colors } from '@material-ui/core';
import { createMuiTheme } from '@material-ui/core/styles';

// Create a theme instance.
const theme = createMuiTheme({
  palette: {
    background: {
      default: '#072136',
    },
    primary: {
      main: "#7C8ABD"
    },
    secondary: {
      main: "#FFFFFF"
    },
    text: {
      primary: '#FFFFFF',
      secondary: '#FFFFFF',
    },
    action: {
      active: "rgba(103, 143, 175, 1)",
      hover:  "rgba(103, 143, 175, 1)",
    }
  }
});

export { theme };
