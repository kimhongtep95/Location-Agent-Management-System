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

import { AgentFormDialog } from "../components/agent-form-dialog";
import { ConfirmDialog } from "../components/confirm-dialog";
import { AgentPayload, api } from "../lib/api";
import { useAuthStore } from "../store/auth-store";
import { Agent, AgentStatus } from "../types/models";

const statusColor: Record<AgentStatus, "default" | "success" | "warning"> = {
  active: "success",
  inactive: "default",
  on_leave: "warning",
};

const statusLabel: Record<AgentStatus, string> = {
  active: "Active",
  inactive: "Inactive",
  on_leave: "On leave",
};

export function AgentsPage() {
  const token = useAuthStore((state) => state.accessToken) ?? "";
  const queryClient = useQueryClient();
  const [statusFilter, setStatusFilter] = useState("");
  const [regionFilter, setRegionFilter] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editing, setEditing] = useState<Agent | null>(null);
  const [deleting, setDeleting] = useState<Agent | null>(null);

  const agentsQuery = useQuery({
    queryKey: ["agents", statusFilter, regionFilter],
    queryFn: () => {
      const params = new URLSearchParams();
      if (statusFilter) params.set("status", statusFilter);
      if (regionFilter) params.set("region", regionFilter);
      return api.getAgents(token, params);
    },
  });

  const invalidate = () => {
    queryClient.invalidateQueries({ queryKey: ["agents"] });
    queryClient.invalidateQueries({ queryKey: ["dashboard"] });
  };

  const saveMutation = useMutation({
    mutationFn: (payload: AgentPayload) =>
      editing ? api.updateAgent(token, editing.id, payload) : api.createAgent(token, payload),
    onSuccess: () => {
      invalidate();
      setDialogOpen(false);
      setEditing(null);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => api.deleteAgent(token, id),
    onSuccess: () => {
      invalidate();
      setDeleting(null);
    },
  });

  const agents = agentsQuery.data ?? [];
  const saveError = saveMutation.error instanceof Error ? saveMutation.error.message : null;

  return (
    <Stack spacing={3}>
      <Stack direction="row" justifyContent="space-between" alignItems="center" flexWrap="wrap" gap={2}>
        <div>
          <Typography variant="overline" sx={{ letterSpacing: 2 }}>
            Roster
          </Typography>
          <Typography variant="h3">Agents</Typography>
        </div>
        <Button
          variant="contained"
          onClick={() => {
            setEditing(null);
            setDialogOpen(true);
          }}
        >
          New Agent
        </Button>
      </Stack>

      {saveError ? <Alert severity="error">{saveError}</Alert> : null}
      {agentsQuery.error instanceof Error ? <Alert severity="error">{agentsQuery.error.message}</Alert> : null}

      <Paper sx={{ p: 3, border: "1px solid rgba(15,23,42,0.08)" }}>
        <Stack direction="row" spacing={2} sx={{ mb: 2 }} flexWrap="wrap">
          <TextField
            label="Status"
            select
            size="small"
            sx={{ minWidth: 160 }}
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value)}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="active">Active</MenuItem>
            <MenuItem value="inactive">Inactive</MenuItem>
            <MenuItem value="on_leave">On leave</MenuItem>
          </TextField>
          <TextField
            label="Region"
            size="small"
            value={regionFilter}
            onChange={(event) => setRegionFilter(event.target.value)}
          />
        </Stack>

        {agentsQuery.isLoading ? (
          <Stack alignItems="center" sx={{ py: 4 }}>
            <CircularProgress />
          </Stack>
        ) : (
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Phone</TableCell>
                <TableCell>Region</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {agents.map((agent) => (
                <TableRow key={agent.id} hover>
                  <TableCell>{agent.full_name}</TableCell>
                  <TableCell>{agent.email}</TableCell>
                  <TableCell>{agent.phone}</TableCell>
                  <TableCell>{agent.region}</TableCell>
                  <TableCell>
                    <Chip size="small" label={statusLabel[agent.status]} color={statusColor[agent.status]} />
                  </TableCell>
                  <TableCell align="right">
                    <Stack direction="row" spacing={1} justifyContent="flex-end">
                      <Button
                        size="small"
                        onClick={() => {
                          setEditing(agent);
                          setDialogOpen(true);
                        }}
                      >
                        Edit
                      </Button>
                      <Button size="small" color="error" onClick={() => setDeleting(agent)}>
                        Delete
                      </Button>
                    </Stack>
                  </TableCell>
                </TableRow>
              ))}
              {agents.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6}>
                    <Typography color="text.secondary" sx={{ py: 2 }}>
                      No agents match these filters.
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : null}
            </TableBody>
          </Table>
        )}
      </Paper>

      {dialogOpen ? (
        <AgentFormDialog
          open={dialogOpen}
          initial={editing}
          submitting={saveMutation.isPending}
          onClose={() => {
            setDialogOpen(false);
            setEditing(null);
          }}
          onSubmit={async (payload) => {
            await saveMutation.mutateAsync(payload);
          }}
        />
      ) : null}

      <ConfirmDialog
        open={Boolean(deleting)}
        title="Delete agent"
        message={`Remove ${deleting?.full_name ?? "this agent"}? This cannot be undone.`}
        loading={deleteMutation.isPending}
        onClose={() => setDeleting(null)}
        onConfirm={() => {
          if (deleting) deleteMutation.mutate(deleting.id);
        }}
      />
    </Stack>
  );
}
