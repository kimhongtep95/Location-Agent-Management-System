import { create } from "zustand";

import { AuthUser } from "../types/models";

interface AuthState {
  accessToken: string | null;
  user: AuthUser | null;
  signIn: (payload: { accessToken: string; user: AuthUser }) => void;
  signOut: () => void;
}

const persistedToken = localStorage.getItem("lams.accessToken");
const persistedUser = localStorage.getItem("lams.user");

export const useAuthStore = create<AuthState>((set) => ({
  accessToken: persistedToken,
  user: persistedUser ? (JSON.parse(persistedUser) as AuthUser) : null,
  signIn: ({ accessToken, user }) => {
    localStorage.setItem("lams.accessToken", accessToken);
    localStorage.setItem("lams.user", JSON.stringify(user));
    set({ accessToken, user });
  },
  signOut: () => {
    localStorage.removeItem("lams.accessToken");
    localStorage.removeItem("lams.user");
    set({ accessToken: null, user: null });
  },
}));
