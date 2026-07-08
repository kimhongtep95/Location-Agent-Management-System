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

import { AssignmentPayload } from "../lib/api";
import { Agent, Location } from "../types/models";

export type AssignmentFormValues = {
  agent_id: string;
  location_id: string;
  notes: string;
};

interface AssignmentFormDialogProps {
  open: boolean;
  agents: Agent[];
  locations: Location[];
  submitting?: boolean;
  onClose: () => void;
  onSubmit: (payload: AssignmentPayload) => Promise<void> | void;
}

export function AssignmentFormDialog({
  open,
  agents,
  locations,
  submitting,
  onClose,
  onSubmit,
}: AssignmentFormDialogProps) {
  const { register, handleSubmit, control } = useForm<AssignmentFormValues>({
    values: {
      agent_id: agents[0]?.id ?? "",
      location_id: locations[0]?.id ?? "",
      notes: "",
    },
  });

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>New assignment</DialogTitle>
      <Stack
        component="form"
        onSubmit={handleSubmit(async (values) => {
          await onSubmit({
            agent_id: values.agent_id,
            location_id: values.location_id,
            notes: values.notes.trim() || null,
          });
        })}
      >
        <DialogContent>
          <Stack spacing={2} sx={{ mt: 1 }}>
            <Controller
              control={control}
              name="agent_id"
              rules={{ required: true }}
              render={({ field }) => (
                <TextField label="Agent" select fullWidth {...field}>
                  {agents.map((agent) => (
                    <MenuItem key={agent.id} value={agent.id}>
                      {agent.full_name} — {agent.region}
                    </MenuItem>
                  ))}
                </TextField>
              )}
            />
            <Controller
              control={control}
              name="location_id"
              rules={{ required: true }}
              render={({ field }) => (
                <TextField label="Location" select fullWidth {...field}>
                  {locations.map((location) => (
                    <MenuItem key={location.id} value={location.id}>
                      {location.name} — {location.city}
                    </MenuItem>
                  ))}
                </TextField>
              )}
            />
            <TextField label="Notes" fullWidth multiline minRows={3} {...register("notes")} />
          </Stack>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 2 }}>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained" disabled={submitting || agents.length === 0 || locations.length === 0}>
            Create assignment
          </Button>
        </DialogActions>
      </Stack>
    </Dialog>
  );
}
