"use client";

import { useEffect, useState } from "react";
import { SessionUser, getSessionUser } from "@/services/auth";

export function useAuth() {
  const [user, setUser] = useState<SessionUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setUser(getSessionUser());
    setLoading(false);
  }, []);

  return { user, loading };
}
