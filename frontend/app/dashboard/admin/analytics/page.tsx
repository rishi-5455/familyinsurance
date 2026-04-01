"use client";

import { useEffect, useState } from "react";
import DashboardShell from "@/components/DashboardShell";
import StatCard from "@/components/StatCard";
import { adminNav } from "@/components/dashboardNav";
import { useRoleGuard } from "@/hooks/useRoleGuard";
import api from "@/services/api";

export default function AnalyticsPage() {
  useRoleGuard(["admin"]);
  const [stats, setStats] = useState<any>({ users: 0, policies: 0, claims: 0, approvedClaims: 0 });

  useEffect(() => {
    api.get("/admin/analytics").then((res) => setStats(res.data)).catch(() => undefined);
  }, []);

  return (
    <DashboardShell title="Admin Dashboard" nav={adminNav}>
      <h1 className="text-2xl font-semibold">Analytics</h1>
      <div className="mt-6 grid gap-4 md:grid-cols-4">
        <StatCard label="Total Users" value={stats.users} />
        <StatCard label="Total Policies" value={stats.policies} />
        <StatCard label="Total Claims" value={stats.claims} />
        <StatCard label="Approved Claims" value={stats.approvedClaims} />
      </div>
    </DashboardShell>
  );
}
