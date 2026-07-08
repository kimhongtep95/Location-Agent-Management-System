import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControlLabel,
  Stack,
  Switch,
  TextField,
} from "@mui/material";
import { Controller, useForm } from "react-hook-form";

import { LocationPayload } from "../lib/api";
import { Location } from "../types/models";

export type LocationFormValues = {
  name: string;
  address: string;
  city: string;
  latitude: number;
  longitude: number;
  is_active: boolean;
};

interface LocationFormDialogProps {
  open: boolean;
  initial?: Location | null;
  submitting?: boolean;
  onClose: () => void;
  onSubmit: (payload: LocationPayload) => Promise<void> | void;
}

export function LocationFormDialog({
  open,
  initial,
  submitting,
  onClose,
  onSubmit,
}: LocationFormDialogProps) {
  const { register, handleSubmit, control } = useForm<LocationFormValues>({
    values: {
      name: initial?.name ?? "",
      address: initial?.address ?? "",
      city: initial?.city ?? "",
      latitude: initial?.latitude ?? 0,
      longitude: initial?.longitude ?? 0,
      is_active: initial?.is_active ?? true,
    },
  });

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{initial ? "Edit location" : "New location"}</DialogTitle>
      <Stack
        component="form"
        onSubmit={handleSubmit(async (values) => {
          await onSubmit({
            name: values.name,
            address: values.address,
            city: values.city,
            latitude: Number(values.latitude),
            longitude: Number(values.longitude),
            is_active: values.is_active,
          });
        })}
      >
        <DialogContent>
          <Stack spacing={2} sx={{ mt: 1 }}>
            <TextField label="Name" fullWidth {...register("name", { required: true })} />
            <TextField label="Address" fullWidth {...register("address", { required: true })} />
            <TextField label="City" fullWidth {...register("city", { required: true })} />
            <Stack direction="row" spacing={2}>
              <TextField
                label="Latitude"
                type="number"
                fullWidth
                inputProps={{ step: "any" }}
                {...register("latitude", { required: true, valueAsNumber: true })}
              />
              <TextField
                label="Longitude"
                type="number"
                fullWidth
                inputProps={{ step: "any" }}
                {...register("longitude", { required: true, valueAsNumber: true })}
              />
            </Stack>
            <Controller
              control={control}
              name="is_active"
              render={({ field }) => (
                <FormControlLabel
                  control={<Switch checked={field.value} onChange={(event) => field.onChange(event.target.checked)} />}
                  label="Active"
                />
              )}
            />
          </Stack>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 2 }}>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained" disabled={submitting}>
            {initial ? "Save changes" : "Create location"}
          </Button>
        </DialogActions>
      </Stack>
    </Dialog>
  );
}
