export type Role = "admin" | "manager" | "agent";

export type AgentStatus = "active" | "inactive" | "on_leave";

export type AssignmentStatus = "assigned" | "checked_in" | "checked_out" | "completed";

export interface AuthUser {
  id: string;
  email: string;
  fullName: string;
  role: Role;
}

export interface Agent {
  id: string;
  full_name: string;
  email: string;
  phone: string;
  region: string;
  status: AgentStatus;
  created_at: string;
}

export interface Location {
  id: string;
  name: string;
  address: string;
  city: string;
  latitude: number;
  longitude: number;
  is_active: boolean;
  created_at: string;
}

export interface Assignment {
  id: string;
  agent_id: string;
  location_id: string;
  status: AssignmentStatus;
  assigned_at: string;
  check_in_at: string | null;
  check_out_at: string | null;
  notes: string | null;
}

export interface DashboardStats {
  total_agents: number;
  agents_by_status: Record<string, number>;
  total_locations: number;
  active_assignments: number;
  checked_in_now: number;
  assignments_by_location: Array<{ location_id: string; location_name: string; count: number }>;
}
