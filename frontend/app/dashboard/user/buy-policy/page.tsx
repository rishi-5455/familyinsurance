"use client";

import { FormEvent, useState, useEffect } from "react";
import DashboardShell from "@/components/DashboardShell";
import { userNav } from "@/components/dashboardNav";
import { useRoleGuard } from "@/hooks/useRoleGuard";
import api from "@/services/api";
import { connectPeraWallet } from "@/services/wallet";

export default function BuyPolicyPage() {
  useRoleGuard(["user"]);
  const [templates, setTemplates] = useState<any[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<any>(null);
  const [walletAddress, setWalletAddress] = useState("");
  const [coverage, setCoverage] = useState("100000");
  const [durationMonths, setDurationMonths] = useState("12");
  const [familyMembers, setFamilyMembers] = useState("[]");
  const [document, setDocument] = useState<File | null>(null);
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load available templates
    api.get("/admin/all-templates")
      .then(({ data }) => {
        setTemplates(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const selectTemplate = (template: any) => {
    setSelectedTemplate(template);
    setCoverage(template.coverage.toString());
    setDurationMonths(template.durationMonths.toString());
  };

  const connectWallet = async () => {
    const account = await connectPeraWallet();
    if (account) setWalletAddress(account);
  };

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    const form = new FormData();
    form.append("coverage", coverage);
    form.append("durationMonths", durationMonths);
    form.append("walletAddress", walletAddress);
    form.append("familyMembers", familyMembers);
    if (document) form.append("document", document);

    try {
      const { data } = await api.post("/user/buy-policy", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMsg(`Policy created: ${data.policy.policyId}`);
    } catch (err: any) {
      setMsg(err?.response?.data?.message || "Could not buy policy");
    }
  };

  return (
    <DashboardShell title="User Dashboard" nav={userNav}>
      <div className="max-w-3xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900">Buy Policy</h1>
          <p className="mt-2 text-slate-600">Purchase a new insurance policy for your family</p>
        </div>

        {/* Available Templates */}
        {loading ? (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-600"></div>
            <p className="mt-2 text-slate-600">Loading templates...</p>
          </div>
        ) : templates.length > 0 && (
          <div className="mb-8">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">Choose a Template</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {templates.map((template) => (
                <button
                  key={template.id}
                  type="button"
                  onClick={() => selectTemplate(template)}
                  className={`text-left p-5 rounded-xl border-2 transition-all ${
                    selectedTemplate?.id === template.id
                      ? 'border-cyan-500 bg-cyan-50 shadow-md'
                      : 'border-slate-200 bg-white hover:border-cyan-300 hover:shadow-sm'
                  }`}
                >
                  <h3 className="font-semibold text-slate-900 mb-2">{template.name}</h3>
                  <div className="space-y-1 text-sm">
                    <p className="text-slate-600">
                      <span className="font-medium">Coverage:</span> ₹{template.coverage?.toLocaleString('en-IN')}
                    </p>
                    <p className="text-slate-600">
                      <span className="font-medium">Duration:</span> {template.durationMonths} months
                    </p>
                    {template.description && (
                      <p className="text-slate-500 text-xs mt-2">{template.description}</p>
                    )}
                  </div>
                  {selectedTemplate?.id === template.id && (
                    <div className="mt-3 flex items-center text-cyan-600 text-sm font-medium">
                      <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                      Selected
                    </div>
                  )}
                </button>
              ))}
            </div>
          </div>
        )}

        <form onSubmit={submit} className="bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="p-8 space-y-6">
            {/* Wallet Section */}
            <div className="pb-6 border-b border-slate-200">
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Wallet Connection (Optional)</h2>
              <div className="space-y-4">
                <button 
                  type="button" 
                  onClick={connectWallet} 
                  className="w-full sm:w-auto px-6 py-3 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition-colors font-medium"
                >
                  {walletAddress ? "✓ Wallet Connected" : "Connect Pera Wallet"}
                </button>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Wallet Address
                  </label>
                  <input 
                    value={walletAddress} 
                    onChange={(e) => setWalletAddress(e.target.value)} 
                    placeholder="Enter Algorand wallet address or connect above" 
                    className="w-full"
                  />
                  <p className="mt-1.5 text-xs text-slate-500">Optional: Link your Algorand wallet for blockchain verification</p>
                </div>
              </div>
            </div>

            {/* Policy Details */}
            <div className="space-y-5">
              <h2 className="text-lg font-semibold text-slate-900">Policy Details</h2>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Coverage Amount <span className="text-red-500">*</span>
                  </label>
                  <div className="relative">
                    <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500">₹</span>
                    <input 
                      value={coverage} 
                      onChange={(e) => setCoverage(e.target.value)} 
                      type="number" 
                      placeholder="500000" 
                      required
                      className="w-full pl-8"
                    />
                  </div>
                  <p className="mt-1.5 text-xs text-slate-500">e.g., 500000 for ₹5 Lakh</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Duration <span className="text-red-500">*</span>
                  </label>
                  <div className="relative">
                    <input 
                      value={durationMonths} 
                      onChange={(e) => setDurationMonths(e.target.value)} 
                      type="number" 
                      placeholder="12" 
                      required
                      className="w-full pr-20"
                    />
                    <span className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 text-sm">months</span>
                  </div>
                  <p className="mt-1.5 text-xs text-slate-500">Policy validity period</p>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Family Members (Optional)
                </label>
                <textarea 
                  value={familyMembers} 
                  onChange={(e) => setFamilyMembers(e.target.value)} 
                  placeholder='[{"name":"Priya Kumar","age":32,"relation":"Spouse"},{"name":"Aarav Kumar","age":5,"relation":"Child"}]' 
                  rows={3}
                  className="w-full font-mono text-xs"
                />
                <p className="mt-1.5 text-xs text-slate-500">Add family members in JSON format or leave empty</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Identity Document (Aadhar/ID)
                </label>
                <input 
                  type="file" 
                  onChange={(e) => setDocument(e.target.files?.[0] || null)}
                  accept=".pdf,.jpg,.jpeg,.png"
                  className="w-full file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-slate-100 file:text-slate-700 hover:file:bg-slate-200 file:cursor-pointer"
                />
                <p className="mt-1.5 text-xs text-slate-500">Upload Aadhar card, passport, or government ID (PDF, JPG, PNG)</p>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="px-8 py-5 bg-slate-50 border-t border-slate-200 rounded-b-xl">
            {msg && (
              <div className={`mb-4 p-4 rounded-lg text-sm ${
                msg.includes('created') 
                  ? 'bg-green-50 text-green-700 border border-green-200' 
                  : 'bg-red-50 text-red-700 border border-red-200'
              }`}>
                {msg}
              </div>
            )}
            <button 
              type="submit"
              className="w-full sm:w-auto px-8 py-3 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 transition-colors font-semibold shadow-sm"
            >
              Purchase Policy
            </button>
          </div>
        </form>
      </div>
    </DashboardShell>
  );
}
