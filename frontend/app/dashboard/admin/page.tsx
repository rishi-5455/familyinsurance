"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import DashboardShell from "@/components/DashboardShell";
import StatCard from "@/components/StatCard";
import { adminNav } from "@/components/dashboardNav";
import { useRoleGuard } from "@/hooks/useRoleGuard";
import api from "@/services/api";

export default function AdminDashboardPage() {
  useRoleGuard(["admin"]);
  const [stats, setStats] = useState<any>({ users: 0, policies: 0, claims: 0, approvedClaims: 0, templates: 0 });
  const [clearing, setClearing] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = () => {
    api.get("/admin/analytics").then((res) => setStats(res.data)).catch(() => undefined);
  };

  const clearTestData = async () => {
    if (!confirm("WARNING: This will delete ALL policies, claims, templates, and notifications. Users will NOT be deleted. Continue?")) {
      return;
    }
    
    setClearing(true);
    try {
      await api.delete("/admin/clear-test-data");
      setMessage("SUCCESS: Test data cleared successfully!");
      loadStats();
      setTimeout(() => setMessage(""), 3000);
    } catch (err: any) {
      setMessage("ERROR: Failed to clear data: " + (err?.response?.data?.message || "Unknown error"));
    } finally {
      setClearing(false);
    }
  };

  return (
    <DashboardShell title="Admin Dashboard" nav={adminNav}>
      <div className="max-w-7xl">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Admin Overview</h1>
            <p className="mt-2 text-slate-600">Monitor system metrics and manage insurance data</p>
          </div>
          <button 
            onClick={clearTestData}
            disabled={clearing}
            className="px-5 py-2.5 text-sm font-medium bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm"
          >
            {clearing ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Clearing...
              </>
            ) : (
              <>
                <svg className="w-4 h-4 inline mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Clear Test Data
              </>
            )}
          </button>
        </div>
      
        {message && (
          <div className={`mb-6 p-5 rounded-xl border ${message.includes("SUCCESS") ? "bg-green-50 text-green-800 border-green-200" : "bg-red-50 text-red-800 border-red-200"}`}>
            <div className="flex gap-3">
              {message.includes("SUCCESS") ? (
                <svg className="w-5 h-5 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg className="w-5 h-5 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              )}
              <p className="font-medium">{message}</p>
            </div>
          </div>
        )}
      
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-5">
          <StatCard label="Total Users" value={stats.users} />
          <StatCard label="Policy Templates" value={stats.templates} />
          <StatCard label="Active Policies" value={stats.policies} />
          <StatCard label="Total Claims" value={stats.claims} />
          <StatCard label="Approved Claims" value={stats.approvedClaims} />
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-3">
          <Link href="/dashboard/admin/create-policy" className="group block bg-gradient-to-br from-cyan-500 to-cyan-600 rounded-xl p-6 text-white hover:from-cyan-600 hover:to-cyan-700 transition-all duration-200 shadow-lg hover:shadow-xl">
            <div className="flex items-center gap-4">
              <div className="bg-white/20 p-3 rounded-lg">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
              </div>
              <div>
                <h3 className="font-semibold text-lg">Create Template</h3>
                <p className="text-sm text-cyan-100">Add new policy blueprint</p>
              </div>
            </div>
          </Link>

          <Link href="/dashboard/admin/view-templates" className="group block bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-xl p-6 text-white hover:from-emerald-600 hover:to-emerald-700 transition-all duration-200 shadow-lg hover:shadow-xl">
            <div className="flex items-center gap-4">
              <div className="bg-white/20 p-3 rounded-lg">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <h3 className="font-semibold text-lg">View Templates</h3>
                <p className="text-sm text-emerald-100">Manage policy templates</p>
              </div>
            </div>
          </Link>

          <Link href="/dashboard/admin/claims-management" className="group block bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-6 text-white hover:from-purple-600 hover:to-purple-700 transition-all duration-200 shadow-lg hover:shadow-xl">
            <div className="flex items-center gap-4">
              <div className="bg-white/20 p-3 rounded-lg">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h3 className="font-semibold text-lg">Claims</h3>
                <p className="text-sm text-purple-100">Review and approve</p>
              </div>
            </div>
          </Link>
        </div>
      </div>
    </DashboardShell>
  );
}
