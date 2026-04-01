"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { Role, getSessionUser } from "@/services/auth";

export function useRoleGuard(allowedRoles: Role[]) {
  const router = useRouter();

  useEffect(() => {
    const user = getSessionUser();
    if (!user || !allowedRoles.includes(user.role)) {
      router.replace("/login");
    }
  }, [allowedRoles, router]);
}
