import { useMutation } from "@tanstack/react-query";
import { Button, Paper, Stack, TextField, Typography } from "@mui/material";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import { api } from "../lib/api";
import { useAuthStore } from "../store/auth-store";

type LoginValues = {
  email: string;
  password: string;
};

export function LoginPage() {
  const navigate = useNavigate();
  const signIn = useAuthStore((state) => state.signIn);
  const { register, handleSubmit } = useForm<LoginValues>({
    defaultValues: {
      email: "admin@lams.local",
      password: "Password123!",
    },
  });

  const loginMutation = useMutation({
    mutationFn: async (values: LoginValues) => {
      const tokens = await api.login(values);
      const user = await api.me(tokens.access_token);
      return { accessToken: tokens.access_token, user };
    },
    onSuccess: ({ accessToken, user }) => {
      signIn({ accessToken, user });
      navigate("/dashboard");
    },
  });
  const errorMessage = loginMutation.error instanceof Error ? loginMutation.error.message : null;

  return (
    <Stack
      minHeight="100vh"
      justifyContent="center"
      alignItems="center"
      sx={{ px: 2, background: "linear-gradient(135deg, #F1F5F9 0%, #E2E8F0 100%)" }}
    >
      <Paper sx={{ maxWidth: 460, width: "100%", p: 4, border: "1px solid rgba(15,23,42,0.1)" }}>
        <Stack spacing={3}>
          <div>
            <Typography variant="overline" sx={{ letterSpacing: 2 }}>
              LAMS Console
            </Typography>
            <Typography variant="h3">Operations sign in</Typography>
            <Typography color="text.secondary">
              Access the console to manage agents, locations, and assignments.
            </Typography>
          </div>
          <Stack component="form" spacing={2} onSubmit={handleSubmit((values) => loginMutation.mutate(values))}>
            <TextField label="Email" fullWidth {...register("email", { required: true })} />
            <TextField label="Password" type="password" fullWidth {...register("password", { required: true })} />
            <Button type="submit" variant="contained" size="large" disabled={loginMutation.isPending}>
              Sign in
            </Button>
          </Stack>
          {errorMessage ? <Typography color="error">{errorMessage}</Typography> : null}
          <Typography variant="body2" color="text.secondary">
            Demo login: admin@lams.local / Password123!
          </Typography>
        </Stack>
      </Paper>
    </Stack>
  );
}
