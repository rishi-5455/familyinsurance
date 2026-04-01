"use client";

export type Role = "admin" | "user" | "verifier";

export interface SessionUser {
  id?: string;
  name: string;
  email: string;
  role: Role;
  walletAddress?: string;
}

export const saveSession = (token: string, user: SessionUser) => {
  localStorage.setItem("token", token);
  localStorage.setItem("user", JSON.stringify(user));
};

export const clearSession = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
};

export const getSessionUser = (): SessionUser | null => {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem("user");
  return raw ? (JSON.parse(raw) as SessionUser) : null;
};
