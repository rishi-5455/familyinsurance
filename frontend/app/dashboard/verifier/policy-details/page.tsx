"use client";

import { useState } from "react";
import DashboardShell from "@/components/DashboardShell";
import { verifierNav } from "@/components/dashboardNav";
import { useRoleGuard } from "@/hooks/useRoleGuard";

export default function PolicyDetailsPage() {
  useRoleGuard(["verifier"]);
  const [note] = useState("Use Verify Policy page to fetch and inspect full policy details.");

  return (
    <DashboardShell title="Verifier Dashboard" nav={verifierNav}>
      <h1 className="text-2xl font-semibold">Policy Details View</h1>
      <p className="mt-4 rounded-lg bg-white border border-slate-200 p-4 text-slate-700">{note}</p>
    </DashboardShell>
  );
}
