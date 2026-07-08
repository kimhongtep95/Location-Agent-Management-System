import AssignmentRounded from "@mui/icons-material/AssignmentRounded";
import DashboardRounded from "@mui/icons-material/DashboardRounded";
import LogoutRounded from "@mui/icons-material/LogoutRounded";
import PeopleRounded from "@mui/icons-material/PeopleRounded";
import PlaceRounded from "@mui/icons-material/PlaceRounded";
import TravelExploreRounded from "@mui/icons-material/TravelExploreRounded";
import {
  AppBar,
  Box,
  Button,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Stack,
  Toolbar,
  Typography,
} from "@mui/material";
import { NavLink, Outlet, useNavigate } from "react-router-dom";

import { useAuthStore } from "../store/auth-store";

const drawerWidth = 260;

const navigation = [
  { label: "Dashboard", icon: <DashboardRounded />, to: "/dashboard", end: false },
  { label: "Agents", icon: <PeopleRounded />, to: "/agents", end: false },
  { label: "Locations", icon: <PlaceRounded />, to: "/locations", end: false },
  { label: "Assignments", icon: <AssignmentRounded />, to: "/assignments", end: false },
];

export function AppShell() {
  const user = useAuthStore((state) => state.user);
  const signOut = useAuthStore((state) => state.signOut);
  const navigate = useNavigate();

  const handleSignOut = () => {
    signOut();
    navigate("/login");
  };

  return (
    <Box sx={{ display: "flex", minHeight: "100vh", backgroundColor: "background.default" }}>
      <AppBar
        position="fixed"
        elevation={0}
        sx={{
          ml: { md: `${drawerWidth}px` },
          width: { md: `calc(100% - ${drawerWidth}px)` },
          backgroundColor: "rgba(255,255,255,0.9)",
          backdropFilter: "blur(12px)",
          borderBottom: "1px solid rgba(15,23,42,0.1)",
          color: "text.primary",
        }}
      >
        <Toolbar sx={{ justifyContent: "space-between" }}>
          <div>
            <Typography variant="overline" sx={{ letterSpacing: 2 }}>
              Operations Console
            </Typography>
            <Typography variant="h6">Coordinate agents across every location</Typography>
          </div>
          <Stack direction="row" spacing={2} alignItems="center">
            <Typography color="text.secondary">{user?.fullName ?? "Operator"}</Typography>
            <Button variant="outlined" color="inherit" endIcon={<LogoutRounded />} onClick={handleSignOut}>
              Sign out
            </Button>
          </Stack>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          display: { xs: "none", md: "block" },
          width: drawerWidth,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: "border-box",
            borderRight: "1px solid rgba(15,23,42,0.1)",
            background: "linear-gradient(180deg, #0F172A 0%, #1E293B 100%)",
            color: "#FFFFFF",
          },
        }}
      >
        <Toolbar />
        <Stack sx={{ px: 3, py: 4, gap: 3, height: "100%" }}>
          <Stack direction="row" spacing={1.5} alignItems="center">
            <TravelExploreRounded />
            <div>
              <Typography variant="h6">LAMS</Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                Location Agent Management
              </Typography>
            </div>
          </Stack>
          <List sx={{ p: 0 }}>
            {navigation.map((item) => (
              <ListItemButton
                key={item.to}
                component={NavLink}
                to={item.to}
                end={item.end}
                sx={{
                  borderRadius: 2,
                  mb: 1,
                  color: "inherit",
                  "&.active": {
                    backgroundColor: "rgba(255,255,255,0.14)",
                  },
                }}
              >
                <ListItemIcon sx={{ color: "inherit", minWidth: 40 }}>{item.icon}</ListItemIcon>
                <ListItemText primary={item.label} />
              </ListItemButton>
            ))}
          </List>
        </Stack>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: { xs: 2, md: 4 }, mt: 10, ml: { md: `${drawerWidth}px` } }}>
        <Outlet />
      </Box>
    </Box>
  );
}
