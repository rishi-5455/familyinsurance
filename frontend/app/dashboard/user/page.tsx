"use client";

import { useEffect, useState } from "react";
import DashboardShell from "@/components/DashboardShell";
import StatCard from "@/components/StatCard";
import { userNav } from "@/components/dashboardNav";
import { useRoleGuard } from "@/hooks/useRoleGuard";
import api from "@/services/api";

export default function UserDashboardPage() {
  useRoleGuard(["user"]);
  const [stats, setStats] = useState({ policies: 0, claims: 0 });
  const [notifications, setNotifications] = useState<any[]>([]);

  useEffect(() => {
    (async () => {
      const policies = await api.get("/user/policies").catch(() => ({ data: [] }));
      const notes = await api.get("/user/notifications").catch(() => ({ data: [] }));
      setStats({ policies: policies.data.length || 0, claims: 0 });
      setNotifications(notes.data || []);
    })();
  }, []);

  return (
    <DashboardShell title="User Dashboard" nav={userNav}>
      <h1 className="text-2xl font-bold text-slate-900">Welcome, Policy Holder</h1>
      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <StatCard label="My Policies" value={stats.policies} />
        <StatCard label="My Claims" value={stats.claims} />
      </div>
      <section className="mt-8 rounded-xl bg-white border border-slate-200 p-5">
        <h2 className="text-lg font-semibold">Notifications</h2>
        <ul className="mt-3 space-y-2 text-sm text-slate-700">
          {notifications.slice(0, 5).map((n) => (
            <li key={n._id} className="rounded-md bg-slate-50 p-2">{n.message}</li>
          ))}
          {!notifications.length && <li>No notifications yet.</li>}
        </ul>
      </section>
    </DashboardShell>
  );
}
