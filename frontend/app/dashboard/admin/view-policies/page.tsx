"use client";

import { useEffect, useState } from "react";
import DashboardShell from "@/components/DashboardShell";
import { adminNav } from "@/components/dashboardNav";
import { useRoleGuard } from "@/hooks/useRoleGuard";
import api from "@/services/api";

export default function ViewPoliciesPage() {
  useRoleGuard(["admin"]);
  const [policies, setPolicies] = useState<any[]>([]);

  useEffect(() => {
    api.get("/admin/all-policies").then((res) => setPolicies(res.data || [])).catch(() => setPolicies([]));
  }, []);

  return (
    <DashboardShell title="Admin Dashboard" nav={adminNav}>
      <h1 className="text-2xl font-semibold">All User Policies</h1>
      
      <div className="mt-4 mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-800">
        <strong>Note:</strong> These are policies purchased by users (POL-xxx IDs). 
        To see policy templates you created, go to "View Templates".
      </div>
      
      {policies.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-xl border border-slate-200">
          <p className="text-gray-500">No user policies yet. Policies appear here when users buy them.</p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {policies.map((p) => (
            <article key={p.policyId} className="rounded-xl bg-white p-5 border border-slate-200 hover:border-cyan-300 hover:shadow-md transition-all">
              <div className="flex items-start justify-between mb-3">
                <h3 className="font-bold text-lg">{p.policyId}</h3>
                <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
                  p.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                }`}>
                  {p.status}
                </span>
              </div>
              <div className="space-y-2 text-sm">
                <p className="text-slate-600"><strong>User ID:</strong> {p.userId?.substring(0, 12)}...</p>
                <p className="text-slate-600"><strong>Coverage:</strong> <span className="text-lg font-semibold text-cyan-600">₹{(p.coverage || 0).toLocaleString('en-IN')}</span></p>
                <p className="text-slate-600"><strong>Expiry:</strong> {p.expiry ? new Date(p.expiry).toLocaleDateString('en-IN', { day: '2-digit', month: '2-digit', year: 'numeric' }) : 'N/A'}</p>
                {p.walletAddress && (
                  <p className="text-slate-600 text-xs"><strong>Wallet:</strong> {p.walletAddress.substring(0, 20)}...</p>
                )}
              </div>
            </article>
          ))}
        </div>
      )}
    </DashboardShell>
  );
}
