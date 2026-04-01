"use client";

import { FormEvent, useState } from "react";
import DashboardShell from "@/components/DashboardShell";
import { userNav } from "@/components/dashboardNav";
import { useRoleGuard } from "@/hooks/useRoleGuard";
import api from "@/services/api";

export default function UserVerifyPolicyPage() {
  useRoleGuard(["user"]);
  const [policyId, setPolicyId] = useState("");
  const [result, setResult] = useState<any>(null);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const { data } = await api.get(`/verifier/verify-policy/${policyId}`);
      setResult(data);
    } catch (err: any) {
      setResult({ message: err?.response?.data?.message || "Verification failed" });
    }
  };

  return (
    <DashboardShell title="User Dashboard" nav={userNav}>
      <h1 className="text-2xl font-semibold">Verify Policy</h1>
      <form onSubmit={submit} className="mt-6 max-w-xl bg-white rounded-xl p-6 border border-slate-200 space-y-3">
        <input value={policyId} onChange={(e) => setPolicyId(e.target.value)} placeholder="Policy ID" required />
        <button className="bg-brand-700 text-white">Verify</button>
      </form>
      {result && <pre className="mt-4 rounded-lg bg-slate-900 text-slate-100 p-4 text-xs overflow-auto">{JSON.stringify(result, null, 2)}</pre>}
    </DashboardShell>
  );
}
