import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#1E293B",
      dark: "#0F172A",
      light: "#475569",
    },
    secondary: {
      main: "#0D9488",
      light: "#14B8A6",
      dark: "#0F766E",
    },
    background: {
      default: "#F1F5F9",
      paper: "#FFFFFF",
    },
    text: {
      primary: "#0F172A",
      secondary: "#475569",
    },
  },
  shape: {
    borderRadius: 10,
  },
  typography: {
    fontFamily: "\"Inter\", sans-serif",
    h1: { fontFamily: "\"Sora\", sans-serif", fontWeight: 700 },
    h2: { fontFamily: "\"Sora\", sans-serif", fontWeight: 700 },
    h3: { fontFamily: "\"Sora\", sans-serif", fontWeight: 700 },
    h4: { fontFamily: "\"Sora\", sans-serif", fontWeight: 600 },
    h5: { fontFamily: "\"Sora\", sans-serif", fontWeight: 600 },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",
          fontWeight: 600,
        },
      },
    },
  },
});
