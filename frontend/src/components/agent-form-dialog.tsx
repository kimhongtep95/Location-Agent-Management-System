import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  MenuItem,
  Stack,
  TextField,
} from "@mui/material";
import { Controller, useForm } from "react-hook-form";

import { AgentPayload } from "../lib/api";
import { Agent, AgentStatus } from "../types/models";

export type AgentFormValues = {
  full_name: string;
  email: string;
  phone: string;
  region: string;
  status: AgentStatus;
};

interface AgentFormDialogProps {
  open: boolean;
  initial?: Agent | null;
  submitting?: boolean;
  onClose: () => void;
  onSubmit: (payload: AgentPayload) => Promise<void> | void;
}

const statusOptions: Array<{ value: AgentStatus; label: string }> = [
  { value: "active", label: "Active" },
  { value: "inactive", label: "Inactive" },
  { value: "on_leave", label: "On leave" },
];

export function AgentFormDialog({ open, initial, submitting, onClose, onSubmit }: AgentFormDialogProps) {
  const { register, handleSubmit, control } = useForm<AgentFormValues>({
    values: {
      full_name: initial?.full_name ?? "",
      email: initial?.email ?? "",
      phone: initial?.phone ?? "",
      region: initial?.region ?? "",
      status: initial?.status ?? "active",
    },
  });

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{initial ? "Edit agent" : "New agent"}</DialogTitle>
      <Stack
        component="form"
        onSubmit={handleSubmit(async (values) => {
          await onSubmit(values);
        })}
      >
        <DialogContent>
          <Stack spacing={2} sx={{ mt: 1 }}>
            <TextField label="Full name" fullWidth {...register("full_name", { required: true })} />
            <TextField label="Email" type="email" fullWidth {...register("email", { required: true })} />
            <TextField label="Phone" fullWidth {...register("phone", { required: true })} />
            <TextField label="Region" fullWidth {...register("region", { required: true })} />
            <Controller
              control={control}
              name="status"
              render={({ field }) => (
                <TextField label="Status" select fullWidth {...field}>
                  {statusOptions.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </TextField>
              )}
            />
          </Stack>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 2 }}>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained" disabled={submitting}>
            {initial ? "Save changes" : "Create agent"}
          </Button>
        </DialogActions>
      </Stack>
    </Dialog>
  );
}
