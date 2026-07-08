import { CssBaseline, ThemeProvider } from "@mui/material";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Navigate, RouterProvider, createBrowserRouter } from "react-router-dom";

import { AppShell } from "./layouts/app-shell";
import { useAuthStore } from "./store/auth-store";
import { theme } from "./theme";
import { AgentsPage } from "./pages/agents-page";
import { AssignmentsPage } from "./pages/assignments-page";
import { DashboardPage } from "./pages/dashboard-page";
import { LocationsPage } from "./pages/locations-page";
import { LoginPage } from "./pages/login-page";

const queryClient = new QueryClient();

function ProtectedRoute() {
  const token = useAuthStore((state) => state.accessToken);
  return token ? <AppShell /> : <Navigate to="/login" replace />;
}

const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/",
    element: <ProtectedRoute />,
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      { path: "dashboard", element: <DashboardPage /> },
      { path: "agents", element: <AgentsPage /> },
      { path: "locations", element: <LocationsPage /> },
      { path: "assignments", element: <AssignmentsPage /> },
    ],
  },
  {
    path: "*",
    element: <Navigate to="/dashboard" replace />,
  },
]);

export function AppRouter() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </ThemeProvider>
  );
}
