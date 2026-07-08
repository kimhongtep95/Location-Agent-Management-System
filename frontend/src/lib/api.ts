import {
  Agent,
  AgentStatus,
  Assignment,
  AuthUser,
  DashboardStats,
  Location,
} from "../types/models";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

type HttpMethod = "GET" | "POST" | "PATCH" | "DELETE";

async function request<T>(path: string, method: HttpMethod, token?: string, body?: unknown): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({ detail: "Request failed." }));
    throw new Error(payload.detail ?? "Request failed.");
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

interface RawAuthUser {
  id: string;
  email: string;
  full_name: string;
  role: AuthUser["role"];
}

function toAuthUser(raw: RawAuthUser): AuthUser {
  return { id: raw.id, email: raw.email, fullName: raw.full_name, role: raw.role };
}

export interface AgentPayload {
  full_name: string;
  email: string;
  phone: string;
  region: string;
  status: AgentStatus;
}

export interface LocationPayload {
  name: string;
  address: string;
  city: string;
  latitude: number;
  longitude: number;
  is_active: boolean;
}

export interface AssignmentPayload {
  agent_id: string;
  location_id: string;
  notes?: string | null;
}

export const api = {
  // ---- Auth ----
  login: (payload: { email: string; password: string }) =>
    request<{ access_token: string; token_type: string }>("/auth/login", "POST", undefined, payload),
  me: async (token: string) => toAuthUser(await request<RawAuthUser>("/auth/me", "GET", token)),

  // ---- Agents ----
  getAgents: (token: string, params: URLSearchParams) =>
    request<Agent[]>(`/agents?${params.toString()}`, "GET", token),
  getAgent: (token: string, id: string) => request<Agent>(`/agents/${id}`, "GET", token),
  createAgent: (token: string, payload: AgentPayload) =>
    request<Agent>("/agents", "POST", token, payload),
  updateAgent: (token: string, id: string, payload: Partial<AgentPayload>) =>
    request<Agent>(`/agents/${id}`, "PATCH", token, payload),
  deleteAgent: (token: string, id: string) => request<void>(`/agents/${id}`, "DELETE", token),

  // ---- Locations ----
  getLocations: (token: string, params: URLSearchParams) =>
    request<Location[]>(`/locations?${params.toString()}`, "GET", token),
  getLocation: (token: string, id: string) => request<Location>(`/locations/${id}`, "GET", token),
  createLocation: (token: string, payload: LocationPayload) =>
    request<Location>("/locations", "POST", token, payload),
  updateLocation: (token: string, id: string, payload: Partial<LocationPayload>) =>
    request<Location>(`/locations/${id}`, "PATCH", token, payload),
  deleteLocation: (token: string, id: string) => request<void>(`/locations/${id}`, "DELETE", token),

  // ---- Assignments ----
  getAssignments: (token: string, params: URLSearchParams) =>
    request<Assignment[]>(`/assignments?${params.toString()}`, "GET", token),
  createAssignment: (token: string, payload: AssignmentPayload) =>
    request<Assignment>("/assignments", "POST", token, payload),
  checkInAssignment: (token: string, id: string) =>
    request<Assignment>(`/assignments/${id}/check-in`, "POST", token),
  checkOutAssignment: (token: string, id: string) =>
    request<Assignment>(`/assignments/${id}/check-out`, "POST", token),

  // ---- Dashboard ----
  getDashboard: (token: string) => request<DashboardStats>("/dashboard/stats", "GET", token),
};
