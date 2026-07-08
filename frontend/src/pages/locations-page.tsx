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

import { ConfirmDialog } from "../components/confirm-dialog";
import { LocationFormDialog } from "../components/location-form-dialog";
import { LocationPayload, api } from "../lib/api";
import { useAuthStore } from "../store/auth-store";
import { Location } from "../types/models";

export function LocationsPage() {
  const token = useAuthStore((state) => state.accessToken) ?? "";
  const queryClient = useQueryClient();
  const [activeFilter, setActiveFilter] = useState("");
  const [cityFilter, setCityFilter] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editing, setEditing] = useState<Location | null>(null);
  const [deleting, setDeleting] = useState<Location | null>(null);

  const locationsQuery = useQuery({
    queryKey: ["locations", activeFilter, cityFilter],
    queryFn: () => {
      const params = new URLSearchParams();
      if (activeFilter) params.set("is_active", activeFilter);
      if (cityFilter) params.set("city", cityFilter);
      return api.getLocations(token, params);
    },
  });

  const invalidate = () => {
    queryClient.invalidateQueries({ queryKey: ["locations"] });
    queryClient.invalidateQueries({ queryKey: ["dashboard"] });
  };

  const saveMutation = useMutation({
    mutationFn: (payload: LocationPayload) =>
      editing ? api.updateLocation(token, editing.id, payload) : api.createLocation(token, payload),
    onSuccess: () => {
      invalidate();
      setDialogOpen(false);
      setEditing(null);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => api.deleteLocation(token, id),
    onSuccess: () => {
      invalidate();
      setDeleting(null);
    },
  });

  const locations = locationsQuery.data ?? [];
  const saveError = saveMutation.error instanceof Error ? saveMutation.error.message : null;

  return (
    <Stack spacing={3}>
      <Stack direction="row" justifyContent="space-between" alignItems="center" flexWrap="wrap" gap={2}>
        <div>
          <Typography variant="overline" sx={{ letterSpacing: 2 }}>
            Coverage
          </Typography>
          <Typography variant="h3">Locations</Typography>
        </div>
        <Button
          variant="contained"
          onClick={() => {
            setEditing(null);
            setDialogOpen(true);
          }}
        >
          New Location
        </Button>
      </Stack>

      {saveError ? <Alert severity="error">{saveError}</Alert> : null}
      {locationsQuery.error instanceof Error ? (
        <Alert severity="error">{locationsQuery.error.message}</Alert>
      ) : null}

      <Paper sx={{ p: 3, border: "1px solid rgba(15,23,42,0.08)" }}>
        <Stack direction="row" spacing={2} sx={{ mb: 2 }} flexWrap="wrap">
          <TextField
            label="Active"
            select
            size="small"
            sx={{ minWidth: 160 }}
            value={activeFilter}
            onChange={(event) => setActiveFilter(event.target.value)}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="true">Active</MenuItem>
            <MenuItem value="false">Inactive</MenuItem>
          </TextField>
          <TextField
            label="City"
            size="small"
            value={cityFilter}
            onChange={(event) => setCityFilter(event.target.value)}
          />
        </Stack>

        {locationsQuery.isLoading ? (
          <Stack alignItems="center" sx={{ py: 4 }}>
            <CircularProgress />
          </Stack>
        ) : (
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell>Address</TableCell>
                <TableCell>City</TableCell>
                <TableCell align="right">Lat</TableCell>
                <TableCell align="right">Lng</TableCell>
                <TableCell>Active</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {locations.map((location) => (
                <TableRow key={location.id} hover>
                  <TableCell>{location.name}</TableCell>
                  <TableCell>{location.address}</TableCell>
                  <TableCell>{location.city}</TableCell>
                  <TableCell align="right">{location.latitude}</TableCell>
                  <TableCell align="right">{location.longitude}</TableCell>
                  <TableCell>
                    <Chip
                      size="small"
                      label={location.is_active ? "Active" : "Inactive"}
                      color={location.is_active ? "success" : "default"}
                    />
                  </TableCell>
                  <TableCell align="right">
                    <Stack direction="row" spacing={1} justifyContent="flex-end">
                      <Button
                        size="small"
                        onClick={() => {
                          setEditing(location);
                          setDialogOpen(true);
                        }}
                      >
                        Edit
                      </Button>
                      <Button size="small" color="error" onClick={() => setDeleting(location)}>
                        Delete
                      </Button>
                    </Stack>
                  </TableCell>
                </TableRow>
              ))}
              {locations.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={7}>
                    <Typography color="text.secondary" sx={{ py: 2 }}>
                      No locations match these filters.
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : null}
            </TableBody>
          </Table>
        )}
      </Paper>

      {dialogOpen ? (
        <LocationFormDialog
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
        title="Delete location"
        message={`Remove ${deleting?.name ?? "this location"}? This cannot be undone.`}
        loading={deleteMutation.isPending}
        onClose={() => setDeleting(null)}
        onConfirm={() => {
          if (deleting) deleteMutation.mutate(deleting.id);
        }}
      />
    </Stack>
  );
}
