"use client";

import { FormEvent, useState } from "react";
import DashboardShell from "@/components/DashboardShell";
import { adminNav } from "@/components/dashboardNav";
import { useRoleGuard } from "@/hooks/useRoleGuard";
import api from "@/services/api";

export default function CreatePolicyPage() {
  useRoleGuard(["admin"]);
  const [form, setForm] = useState({ name: "", coverage: "", durationMonths: "12", description: "" });
  const [msg, setMsg] = useState("");

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const { data } = await api.post("/admin/create-policy", form);
      setMsg(`Template created: ${data.template.templateId}`);
    } catch (err: any) {
      setMsg(err?.response?.data?.message || "Failed");
    }
  };

  return (
    <DashboardShell title="Admin Dashboard" nav={adminNav}>
      <div className="max-w-3xl">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-slate-900">Create Policy Template</h1>
          <p className="mt-2 text-slate-600">Design a policy template that users can purchase</p>
        </div>

        <div className="bg-amber-50 border border-amber-200 p-5 rounded-xl mb-8">
          <div className="flex gap-3">
            <svg className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <div>
              <p className="text-sm font-medium text-amber-900">About Policy Templates</p>
              <p className="mt-1 text-sm text-amber-800">
                Templates are policy blueprints. After creating, view them in "View Templates". 
                User-purchased policies appear in "View Policies".
              </p>
            </div>
          </div>
        </div>
      
        <form onSubmit={submit} className="bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="p-8 space-y-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Policy Name <span className="text-red-500">*</span>
              </label>
              <input 
                value={form.name} 
                onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))} 
                placeholder="e.g., Family Health Premium, Senior Citizen Care" 
                required
                className="w-full"
              />
              <p className="mt-1.5 text-xs text-slate-500">Choose a descriptive name for this policy template</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Coverage Amount <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 font-medium">₹</span>
                  <input 
                    value={form.coverage} 
                    onChange={(e) => setForm((p) => ({ ...p, coverage: e.target.value }))} 
                    type="number" 
                    placeholder="500000" 
                    required
                    className="w-full pl-8"
                  />
                </div>
                <p className="mt-1.5 text-xs text-slate-500">Maximum coverage (e.g., 500000 = ₹5 Lakh)</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Duration <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <input 
                    value={form.durationMonths} 
                    onChange={(e) => setForm((p) => ({ ...p, durationMonths: e.target.value }))} 
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
                Description (Optional)
              </label>
              <textarea 
                value={form.description} 
                onChange={(e) => setForm((p) => ({ ...p, description: e.target.value }))} 
                placeholder="Describe coverage details, benefits, terms and conditions..." 
                rows={4}
                className="w-full"
              />
              <p className="mt-1.5 text-xs text-slate-500">Provide additional details about this policy</p>
            </div>
          </div>

          <div className="px-8 py-5 bg-slate-50 border-t border-slate-200 rounded-b-xl">
            {msg && (
              <div className={`mb-4 p-4 rounded-lg text-sm border ${
                msg.includes('created') 
                  ? 'bg-green-50 text-green-700 border-green-200' 
                  : 'bg-red-50 text-red-700 border-red-200'
              }`}>
                {msg}
              </div>
            )}
            <button 
              type="submit"
              className="w-full sm:w-auto px-8 py-3 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 transition-colors font-semibold shadow-sm"
            >
              Create Template
            </button>
          </div>
        </form>
      </div>
    </DashboardShell>
  );
}
