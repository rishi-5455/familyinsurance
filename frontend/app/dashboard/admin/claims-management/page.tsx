"use client";

import { useEffect, useState } from "react";
import DashboardShell from "@/components/DashboardShell";
import { adminNav } from "@/components/dashboardNav";
import { useRoleGuard } from "@/hooks/useRoleGuard";
import api from "@/services/api";

interface Claim {
  id: string;
  claimId: string;
  policyId: string;
  userId: string;
  amount: number;
  description: string;
  status: string;
  submittedAt: string;
}

export default function ClaimsManagementPage() {
  useRoleGuard(["admin"]);
  const [claims, setClaims] = useState<Claim[]>([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadClaims();
  }, []);

  const loadClaims = async () => {
    try {
      const { data } = await api.get("/admin/all-claims");
      setClaims(data || []);
    } catch (err) {
      console.error("Failed to load claims", err);
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (claimId: string, action: string) => {
    try {
      const { data } = await api.post("/admin/approve-claim", { claimId, action });
      setMessage(data.message);
      // Reload claims to show updated status
      loadClaims();
      setTimeout(() => setMessage(""), 3000);
    } catch (err: any) {
      setMessage(err?.response?.data?.message || "Action failed");
      setTimeout(() => setMessage(""), 3000);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "approved":
        return "text-green-700 bg-green-50";
      case "rejected":
        return "text-red-700 bg-red-50";
      default:
        return "text-yellow-700 bg-yellow-50";
    }
  };

  return (
    <DashboardShell title="Admin Dashboard" nav={adminNav}>
      <div className="max-w-7xl">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Claims Management</h1>
            <p className="mt-2 text-slate-600">Review and process insurance claims</p>
          </div>
          <button
            onClick={loadClaims}
            className="px-5 py-2.5 text-sm font-medium bg-white border border-slate-200 hover:bg-slate-50 rounded-lg transition-colors shadow-sm"
          >
            <svg className="w-4 h-4 inline mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Refresh
          </button>
        </div>

        {message && (
          <div className="mb-6 p-5 rounded-xl bg-blue-50 border border-blue-200">
            <div className="flex gap-3">
              <svg className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
              <p className="text-sm font-medium text-blue-900">{message}</p>
            </div>
          </div>
        )}

        {loading ? (
          <div className="bg-white rounded-xl border border-slate-200 p-16 text-center">
            <div className="inline-block h-10 w-10 animate-spin rounded-full border-4 border-solid border-cyan-600 border-r-transparent mb-4"></div>
            <p className="text-slate-500">Loading claims...</p>
          </div>
        ) : claims.length === 0 ? (
          <div className="bg-white rounded-xl border-2 border-dashed border-slate-300 p-16 text-center">
            <svg className="mx-auto h-16 w-16 text-slate-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p className="text-lg font-medium text-slate-900 mb-2">No claims found</p>
            <p className="text-sm text-slate-500">Claims submitted by users will appear here</p>
          </div>
        ) : (
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-50 border-b border-slate-200">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Claim ID</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Policy ID</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">User ID</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Amount</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Description</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200">
                  {claims.map((claim) => (
                    <tr key={claim.id} className="hover:bg-slate-50 transition-colors">
                      <td className="px-6 py-4 text-sm font-mono font-medium text-slate-900">{claim.claimId}</td>
                      <td className="px-6 py-4 text-sm font-mono text-slate-600">{claim.policyId}</td>
                      <td className="px-6 py-4 text-sm text-slate-600 truncate max-w-[100px]">{claim.userId}</td>
                      <td className="px-6 py-4 text-sm font-semibold text-slate-900">₹{claim.amount?.toLocaleString('en-IN')}</td>
                      <td className="px-6 py-4 text-sm text-slate-600 max-w-xs truncate">{claim.description}</td>
                      <td className="px-6 py-4">
                        <span className={`px-3 py-1 text-xs font-semibold rounded-full uppercase ${getStatusColor(claim.status)}`}>
                          {claim.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm space-x-2">
                        {(claim.status === "pending" || claim.status === "submitted") ? (
                          <>
                            <button
                              onClick={() => handleAction(claim.claimId, "approve")}
                              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium shadow-sm"
                            >
                              Approve
                            </button>
                            <button
                              onClick={() => handleAction(claim.claimId, "reject")}
                              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium shadow-sm"
                            >
                              Reject
                            </button>
                          </>
                        ) : (
                          <span className="text-slate-500 text-sm">
                            {claim.status === 'approved' && '✓ Already approved'}
                            {claim.status === 'rejected' && '✗ Already rejected'}
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </DashboardShell>
  );
}
