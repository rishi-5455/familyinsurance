"use client";

import { useEffect, useState } from "react";
import DashboardShell from "@/components/DashboardShell";
import { adminNav } from "@/components/dashboardNav";
import { useRoleGuard } from "@/hooks/useRoleGuard";
import api from "@/services/api";

export default function ViewUsersPage() {
  useRoleGuard(["admin"]);
  const [users, setUsers] = useState<any[]>([]);

  useEffect(() => {
    api.get("/admin/users").then((res) => setUsers(res.data || [])).catch(() => setUsers([]));
  }, []);

  return (
    <DashboardShell title="Admin Dashboard" nav={adminNav}>
      <h1 className="text-2xl font-semibold">Users</h1>
      <div className="mt-6 overflow-auto rounded-xl bg-white border border-slate-200">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-100 text-left">
            <tr>
              <th className="p-3">Name</th>
              <th className="p-3">Email</th>
              <th className="p-3">Role</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u._id} className="border-t border-slate-200">
                <td className="p-3">{u.name}</td>
                <td className="p-3">{u.email}</td>
                <td className="p-3 uppercase">{u.role}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </DashboardShell>
  );
}
