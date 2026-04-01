"use client";

import { FormEvent, useState } from "react";
import DashboardShell from "@/components/DashboardShell";
import { userNav } from "@/components/dashboardNav";
import { useRoleGuard } from "@/hooks/useRoleGuard";
import api from "@/services/api";

export default function SubmitClaimPage() {
  useRoleGuard(["user"]);
  const [policyId, setPolicyId] = useState("");
  const [amount, setAmount] = useState("");
  const [reason, setReason] = useState("");
  const [document, setDocument] = useState<File | null>(null);
  const [message, setMessage] = useState("");

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    const form = new FormData();
    form.append("policyId", policyId);
    form.append("amount", amount);
    form.append("reason", reason);
    if (document) form.append("document", document);

    try {
      const { data } = await api.post("/claims/submit-claim", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage(`Claim submitted: ${data.claim.claimId}`);
    } catch (err: any) {
      setMessage(err?.response?.data?.message || "Failed to submit claim");
    }
  };

  return (
    <DashboardShell title="User Dashboard" nav={userNav}>
      <div className="max-w-3xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900">Submit Insurance Claim</h1>
          <p className="mt-2 text-slate-600">File a claim for medical expenses covered by your policy</p>
        </div>

        <form onSubmit={submit} className="bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="p-8 space-y-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Policy ID <span className="text-red-500">*</span>
              </label>
              <input 
                value={policyId} 
                onChange={(e) => setPolicyId(e.target.value)} 
                placeholder="POL-XXXXXXXXXX" 
                required
                className="w-full font-mono"
              />
              <p className="mt-1.5 text-xs text-slate-500">Enter the policy ID you want to claim under</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Claim Amount <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 font-medium">₹</span>
                <input 
                  type="number"
                  value={amount} 
                  onChange={(e) => setAmount(e.target.value)} 
                  placeholder="50000" 
                  required
                  min="1"
                  className="w-full pl-8"
                />
              </div>
              <p className="mt-1.5 text-xs text-slate-500">Enter the total claim amount for medical expenses</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Reason for Claim <span className="text-red-500">*</span>
              </label>
              <textarea 
                value={reason} 
                onChange={(e) => setReason(e.target.value)} 
                placeholder="Describe the medical treatment, hospitalization details, diagnosis, etc." 
                required 
                rows={5}
                className="w-full"
              />
              <p className="mt-1.5 text-xs text-slate-500">Provide detailed information about your claim</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Supporting Documents
              </label>
              <input 
                type="file" 
                onChange={(e) => setDocument(e.target.files?.[0] || null)}
                accept=".pdf,.jpg,.jpeg,.png"
                className="w-full file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-slate-100 file:text-slate-700 hover:file:bg-slate-200 file:cursor-pointer"
              />
              <p className="mt-1.5 text-xs text-slate-500">Upload hospital bills, medical reports, prescriptions (PDF, JPG, PNG)</p>
            </div>
          </div>

          <div className="px-8 py-5 bg-slate-50 border-t border-slate-200 rounded-b-xl">
            {message && (
              <div className={`mb-4 p-4 rounded-lg text-sm border ${
                message.includes('submitted') 
                  ? 'bg-green-50 text-green-700 border-green-200' 
                  : 'bg-red-50 text-red-700 border-red-200'
              }`}>
                {message}
              </div>
            )}
            <button 
              type="submit"
              className="w-full sm:w-auto px-8 py-3 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 transition-colors font-semibold shadow-sm"
            >
              Submit Claim
            </button>
          </div>
        </form>
      </div>
    </DashboardShell>
  );
}
