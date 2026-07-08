import { ArcElement, BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, Tooltip } from "chart.js";
import Grid from "@mui/material/Grid2";
import { useQuery } from "@tanstack/react-query";
import { Bar, Doughnut } from "react-chartjs-2";
import { Alert, CircularProgress, Paper, Stack, Typography } from "@mui/material";

import { StatCard } from "../components/stat-card";
import { api } from "../lib/api";
import { useAuthStore } from "../store/auth-store";

ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Legend, Tooltip);

const statusLabels: Record<string, string> = {
  active: "Active",
  inactive: "Inactive",
  on_leave: "On leave",
};

const statusColors = ["#0D9488", "#94A3B8", "#F59E0B", "#1E293B", "#B91C1C"];

export function DashboardPage() {
  const token = useAuthStore((state) => state.accessToken);
  const dashboardQuery = useQuery({
    queryKey: ["dashboard"],
    queryFn: () => api.getDashboard(token ?? ""),
    enabled: Boolean(token),
  });

  const data = dashboardQuery.data;
  const statusEntries = Object.entries(data?.agents_by_status ?? {});
  const byLocation = data?.assignments_by_location ?? [];

  return (
    <Stack spacing={3}>
      <div>
        <Typography variant="overline" sx={{ letterSpacing: 2 }}>
          Operations Overview
        </Typography>
        <Typography variant="h3">Field operations at a glance</Typography>
        <Typography color="text.secondary">
          Monitor your agent roster, coverage locations, and live check-ins.
        </Typography>
      </div>

      {dashboardQuery.isLoading ? (
        <Stack alignItems="center" sx={{ py: 6 }}>
          <CircularProgress />
        </Stack>
      ) : null}

      {dashboardQuery.error instanceof Error ? (
        <Alert severity="error">{dashboardQuery.error.message}</Alert>
      ) : null}

      <Grid container spacing={2}>
        <Grid size={{ xs: 6, md: 3 }}>
          <StatCard eyebrow="Agents" value={`${data?.total_agents ?? 0}`} helper="Total roster" />
        </Grid>
        <Grid size={{ xs: 6, md: 3 }}>
          <StatCard eyebrow="Locations" value={`${data?.total_locations ?? 0}`} helper="Coverage points" />
        </Grid>
        <Grid size={{ xs: 6, md: 3 }}>
          <StatCard eyebrow="Active" value={`${data?.active_assignments ?? 0}`} helper="Open assignments" />
        </Grid>
        <Grid size={{ xs: 6, md: 3 }}>
          <StatCard eyebrow="On site" value={`${data?.checked_in_now ?? 0}`} helper="Checked in now" />
        </Grid>
      </Grid>

      <Grid container spacing={2}>
        <Grid size={{ xs: 12, lg: 5 }}>
          <Paper sx={{ p: 3, border: "1px solid rgba(15,23,42,0.08)", height: "100%" }}>
            <Typography variant="h5" sx={{ mb: 2 }}>
              Agents by Status
            </Typography>
            {statusEntries.length === 0 ? (
              <Typography color="text.secondary">No agents yet.</Typography>
            ) : (
              <Doughnut
                data={{
                  labels: statusEntries.map(([key]) => statusLabels[key] ?? key),
                  datasets: [
                    {
                      data: statusEntries.map(([, count]) => count),
                      backgroundColor: statusColors,
                      borderWidth: 0,
                    },
                  ],
                }}
              />
            )}
          </Paper>
        </Grid>
        <Grid size={{ xs: 12, lg: 7 }}>
          <Paper sx={{ p: 3, border: "1px solid rgba(15,23,42,0.08)", height: "100%" }}>
            <Typography variant="h5" sx={{ mb: 2 }}>
              Assignments by Location
            </Typography>
            {byLocation.length === 0 ? (
              <Typography color="text.secondary">No assignments yet.</Typography>
            ) : (
              <Bar
                data={{
                  labels: byLocation.map((row) => row.location_name),
                  datasets: [
                    {
                      label: "Assignments",
                      data: byLocation.map((row) => row.count),
                      backgroundColor: "#0D9488",
                      borderRadius: 8,
                    },
                  ],
                }}
                options={{ responsive: true, plugins: { legend: { display: false } } }}
              />
            )}
          </Paper>
        </Grid>
      </Grid>
    </Stack>
  );
}
