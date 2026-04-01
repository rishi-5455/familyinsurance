"use client";

import { FormEvent, useState } from "react";
import DashboardShell from "@/components/DashboardShell";
import { verifierNav } from "@/components/dashboardNav";
import { useRoleGuard } from "@/hooks/useRoleGuard";
import api from "@/services/api";

export default function VerifierPage() {
  useRoleGuard(["verifier"]);
  const [policyId, setPolicyId] = useState("");
  const [result, setResult] = useState<any>(null);

  const verify = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const { data } = await api.get(`/verifier/verify-policy/${policyId}`);
      setResult(data);
    } catch (err: any) {
      setResult({ message: err?.response?.data?.message || "Unable to verify" });
    }
  };

  return (
    <DashboardShell title="Verifier Dashboard" nav={verifierNav}>
      <div className="max-w-5xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900">Verify Policy</h1>
          <p className="mt-2 text-slate-600">Authenticate insurance policies through blockchain verification</p>
        </div>

        <form onSubmit={verify} className="bg-white rounded-xl border border-slate-200 shadow-sm mb-8">
          <div className="p-8">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Policy ID <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <input 
                  value={policyId} 
                  onChange={(e) => setPolicyId(e.target.value)} 
                  placeholder="POL-XXXXXXXXXX" 
                  required
                  className="w-full font-mono pr-12"
                />
                <svg className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <p className="mt-1.5 text-xs text-slate-500">Enter the policy ID from patient's insurance card or QR code</p>
            </div>
          </div>

          <div className="px-8 py-5 bg-slate-50 border-t border-slate-200 rounded-b-xl">
            <button 
              type="submit"
              className="w-full sm:w-auto px-8 py-3 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 transition-colors font-semibold shadow-sm"
            >
              <svg className="w-5 h-5 inline mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Verify Policy
            </button>
          </div>
        </form>

        {result && (
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="px-6 py-4 bg-slate-50 border-b border-slate-200">
              <h2 className="text-lg font-semibold text-slate-900">Verification Result</h2>
            </div>
            
            {result.policy ? (
              <div className="p-6">
                <div className="flex items-start gap-4 mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
                  <svg className="w-6 h-6 text-green-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <div>
                    <p className="font-semibold text-green-900 mb-1">✓ Policy Verified</p>
                    <p className="text-sm text-green-800">This is a valid, blockchain-verified insurance policy</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-sm font-medium text-slate-500 mb-3">Policy Information</h3>
                    <div className="space-y-3">
                      <div>
                        <p className="text-xs text-slate-500">Policy ID</p>
                        <p className="text-sm font-mono font-semibold text-slate-900 mt-1">{result.policy.policyId}</p>
                      </div>
                      <div>
                        <p className="text-xs text-slate-500">Coverage Amount</p>
                        <p className="text-lg font-bold text-green-600 mt-1">₹{result.policy.coverage?.toLocaleString('en-IN')}</p>
                      </div>
                      <div>
                        <p className="text-xs text-slate-500">Status</p>
                        <span className={`inline-block mt-1 px-3 py-1 text-xs font-semibold rounded-full ${
                          result.policy.status === 'active' 
                            ? 'bg-green-100 text-green-700' 
                            : 'bg-gray-100 text-gray-700'
                        }`}>
                          {result.policy.status}
                        </span>
                      </div>
                      {result.policy.expiry && (
                        <div>
                          <p className="text-xs text-slate-500">Expiry Date</p>
                          <p className="text-sm font-medium text-slate-900 mt-1">
                            {new Date(result.policy.expiry).toLocaleDateString('en-IN', { 
                              day: '2-digit', 
                              month: 'long', 
                              year: 'numeric' 
                            })}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>

                  <div>
                    <h3 className="text-sm font-medium text-slate-500 mb-3">Blockchain Verification</h3>
                    <div className="space-y-3">
                      {result.blockchain ? (
                        <>
                          <div>
                            <p className="text-xs text-slate-500">Verification Status</p>
                            <div className="flex items-center gap-2 mt-1">
                              <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                              </svg>
                              <span className="text-sm font-semibold text-green-700">Verified on Blockchain</span>
                            </div>
                          </div>
                          {result.blockchain.transactionId && (
                            <div>
                              <p className="text-xs text-slate-500">Transaction ID</p>
                              <p className="text-xs font-mono break-all text-slate-600 mt-1">{result.blockchain.transactionId}</p>
                            </div>
                          )}
                        </>
                      ) : (
                        <div className="flex items-center gap-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                          <svg className="w-5 h-5 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                          </svg>
                          <p className="text-sm text-yellow-800">Blockchain verification pending</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                <div className="mt-6 pt-6 border-t border-slate-200">
                  <h3 className="text-sm font-medium text-slate-500 mb-3">Raw Data (JSON)</h3>
                  <pre className="text-xs bg-slate-900 text-slate-100 p-4 rounded-lg overflow-auto max-h-96">
{JSON.stringify(result, null, 2)}
                  </pre>
                </div>
              </div>
            ) : (
              <div className="p-6">
                <div className="flex items-start gap-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <svg className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                  <div>
                    <p className="font-semibold text-red-900 mb-1">✗ Verification Failed</p>
                    <p className="text-sm text-red-800">{result.message}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </DashboardShell>
  );
}
