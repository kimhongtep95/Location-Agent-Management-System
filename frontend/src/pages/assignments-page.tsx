import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Alert,
  Button,
  Chip,
  CircularProgress,
  MenuItem,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";

import { AssignmentFormDialog } from "../components/assignment-form-dialog";
import { AssignmentPayload, api } from "../lib/api";
import { useAuthStore } from "../store/auth-store";
import { AssignmentStatus } from "../types/models";

const statusColor: Record<AssignmentStatus, "default" | "info" | "success" | "warning"> = {
  assigned: "info",
  checked_in: "success",
  checked_out: "warning",
  completed: "default",
};

const statusLabel: Record<AssignmentStatus, string> = {
  assigned: "Assigned",
  checked_in: "Checked in",
  checked_out: "Checked out",
  completed: "Completed",
};

function formatTimestamp(value: string | null): string {
  if (!value) return "—";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "—" : date.toLocaleString();
}

export function AssignmentsPage() {
  const token = useAuthStore((state) => state.accessToken) ?? "";
  const queryClient = useQueryClient();
  const [statusFilter, setStatusFilter] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);

  const assignmentsQuery = useQuery({
    queryKey: ["assignments", statusFilter],
    queryFn: () => {
      const params = new URLSearchParams();
      if (statusFilter) params.set("status", statusFilter);
      return api.getAssignments(token, params);
    },
  });

  const agentsQuery = useQuery({
    queryKey: ["agents", "", ""],
    queryFn: () => api.getAgents(token, new URLSearchParams()),
  });

  const locationsQuery = useQuery({
    queryKey: ["locations", "", ""],
    queryFn: () => api.getLocations(token, new URLSearchParams()),
  });

  const invalidate = () => {
    queryClient.invalidateQueries({ queryKey: ["assignments"] });
    queryClient.invalidateQueries({ queryKey: ["dashboard"] });
  };

  const createMutation = useMutation({
    mutationFn: (payload: AssignmentPayload) => api.createAssignment(token, payload),
    onSuccess: () => {
      invalidate();
      setDialogOpen(false);
    },
  });

  const checkInMutation = useMutation({
    mutationFn: (id: string) => api.checkInAssignment(token, id),
    onSuccess: invalidate,
  });

  const checkOutMutation = useMutation({
    mutationFn: (id: string) => api.checkOutAssignment(token, id),
    onSuccess: invalidate,
  });

  const agents = agentsQuery.data ?? [];
  const locations = locationsQuery.data ?? [];
  const assignments = assignmentsQuery.data ?? [];

  const agentName = (id: string) => agents.find((agent) => agent.id === id)?.full_name ?? id;
  const locationName = (id: string) => locations.find((location) => location.id === id)?.name ?? id;

  const createError = createMutation.error instanceof Error ? createMutation.error.message : null;
  const actionError =
    checkInMutation.error instanceof Error
      ? checkInMutation.error.message
      : checkOutMutation.error instanceof Error
        ? checkOutMutation.error.message
        : null;

  return (
    <Stack spacing={3}>
      <Stack direction="row" justifyContent="space-between" alignItems="center" flexWrap="wrap" gap={2}>
        <div>
          <Typography variant="overline" sx={{ letterSpacing: 2 }}>
            Field Work
          </Typography>
          <Typography variant="h3">Assignments</Typography>
        </div>
        <Button variant="contained" onClick={() => setDialogOpen(true)}>
          New Assignment
        </Button>
      </Stack>

      {createError ? <Alert severity="error">{createError}</Alert> : null}
      {actionError ? <Alert severity="error">{actionError}</Alert> : null}
      {assignmentsQuery.error instanceof Error ? (
        <Alert severity="error">{assignmentsQuery.error.message}</Alert>
      ) : null}

      <Paper sx={{ p: 3, border: "1px solid rgba(15,23,42,0.08)" }}>
        <Stack direction="row" spacing={2} sx={{ mb: 2 }} flexWrap="wrap">
          <TextField
            label="Status"
            select
            size="small"
            sx={{ minWidth: 180 }}
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value)}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="assigned">Assigned</MenuItem>
            <MenuItem value="checked_in">Checked in</MenuItem>
            <MenuItem value="checked_out">Checked out</MenuItem>
            <MenuItem value="completed">Completed</MenuItem>
          </TextField>
        </Stack>

        {assignmentsQuery.isLoading ? (
          <Stack alignItems="center" sx={{ py: 4 }}>
            <CircularProgress />
          </Stack>
        ) : (
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Agent</TableCell>
                <TableCell>Location</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Assigned</TableCell>
                <TableCell>Check-in</TableCell>
                <TableCell>Check-out</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {assignments.map((assignment) => (
                <TableRow key={assignment.id} hover>
                  <TableCell>{agentName(assignment.agent_id)}</TableCell>
                  <TableCell>{locationName(assignment.location_id)}</TableCell>
                  <TableCell>
                    <Chip
                      size="small"
                      label={statusLabel[assignment.status]}
                      color={statusColor[assignment.status]}
                    />
                  </TableCell>
                  <TableCell>{formatTimestamp(assignment.assigned_at)}</TableCell>
                  <TableCell>{formatTimestamp(assignment.check_in_at)}</TableCell>
                  <TableCell>{formatTimestamp(assignment.check_out_at)}</TableCell>
                  <TableCell align="right">
                    <Stack direction="row" spacing={1} justifyContent="flex-end">
                      <Button
                        size="small"
                        variant="outlined"
                        disabled={assignment.status !== "assigned" || checkInMutation.isPending}
                        onClick={() => checkInMutation.mutate(assignment.id)}
                      >
                        Check-in
                      </Button>
                      <Button
                        size="small"
                        variant="outlined"
                        disabled={assignment.status !== "checked_in" || checkOutMutation.isPending}
                        onClick={() => checkOutMutation.mutate(assignment.id)}
                      >
                        Check-out
                      </Button>
                    </Stack>
                  </TableCell>
                </TableRow>
              ))}
              {assignments.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={7}>
                    <Typography color="text.secondary" sx={{ py: 2 }}>
                      No assignments match these filters.
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : null}
            </TableBody>
          </Table>
        )}
      </Paper>

      {dialogOpen ? (
        <AssignmentFormDialog
          open={dialogOpen}
          agents={agents}
          locations={locations}
          submitting={createMutation.isPending}
          onClose={() => setDialogOpen(false)}
          onSubmit={async (payload) => {
            await createMutation.mutateAsync(payload);
          }}
        />
      ) : null}
    </Stack>
  );
}
