"use client";

import { useEffect, useState } from "react";
import { QRCodeSVG } from "qrcode.react";
import DashboardShell from "@/components/DashboardShell";
import { userNav } from "@/components/dashboardNav";
import { useRoleGuard } from "@/hooks/useRoleGuard";
import api from "@/services/api";

export default function MyPoliciesPage() {
  useRoleGuard(["user"]);
  const [policies, setPolicies] = useState<any[]>([]);

  useEffect(() => {
    api.get("/user/policies").then((res) => setPolicies(res.data || [])).catch(() => setPolicies([]));
  }, []);

  return (
    <DashboardShell title="User Dashboard" nav={userNav}>
      <div className="max-w-7xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900">My Insurance Policies</h1>
          <p className="mt-2 text-slate-600">View and manage your purchased insurance policies</p>
        </div>

        {policies.length === 0 ? (
          <div className="bg-white rounded-xl border-2 border-dashed border-slate-300 p-16 text-center">
            <svg className="mx-auto h-16 w-16 text-slate-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p className="text-lg font-medium text-slate-900 mb-2">No policies found</p>
            <p className="text-sm text-slate-500 mb-6">Purchase a policy to get started with insurance coverage</p>
            <a 
              href="/dashboard/user/buy-policy" 
              className="inline-block px-6 py-3 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 transition-colors font-medium shadow-sm"
            >
              Buy Policy
            </a>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {policies.map((policy) => (
              <article 
                key={policy.policyId} 
                className="group bg-white rounded-xl p-6 border border-slate-200 shadow-sm hover:shadow-lg hover:border-cyan-300 transition-all duration-200"
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="font-bold text-lg text-slate-900 group-hover:text-cyan-600 transition-colors">
                      {policy.policyId}
                    </h3>
                    <p className="text-xs text-slate-500 mt-1 font-mono">
                      Policy ID
                    </p>
                  </div>
                  <span className={`px-3 py-1 text-xs font-semibold rounded-full uppercase ${
                    policy.status === 'active' 
                      ? 'bg-green-100 text-green-700' 
                      : 'bg-gray-100 text-gray-700'
                  }`}>
                    {policy.status}
                  </span>
                </div>

                <div className="space-y-3 mb-5">
                  <div className="flex items-center gap-2">
                    <svg className="w-5 h-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <div>
                      <p className="text-xs text-slate-500">Coverage</p>
                      <p className="text-lg font-bold text-slate-900">
                        ₹{Number(policy.coverage)?.toLocaleString('en-IN')}
                      </p>
                    </div>
                  </div>

                  {policy.expiry && (
                    <div className="flex items-center gap-2 text-sm">
                      <svg className="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <div>
                        <p className="text-xs text-slate-500">Expires on</p>
                        <p className="text-sm font-medium text-slate-900">
                          {new Date(policy.expiry).toLocaleDateString('en-IN', { day: '2-digit', month: '2-digit', year: 'numeric' })}
                        </p>
                      </div>
                    </div>
                  )}
                </div>

                <div className="pt-4 border-t border-slate-100">
                  <p className="text-xs text-slate-500 mb-3">Scan QR to verify</p>
                  <div className="bg-white p-3 rounded-lg border border-slate-200 inline-block">
                    <QRCodeSVG value={policy.policyId} size={120} includeMargin={true} />
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}
      </div>
    </DashboardShell>
  );
}
