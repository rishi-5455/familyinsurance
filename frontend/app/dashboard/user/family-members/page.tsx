"use client";

import { FormEvent, useState, useEffect } from "react";
import DashboardShell from "@/components/DashboardShell";
import { userNav } from "@/components/dashboardNav";
import { useRoleGuard } from "@/hooks/useRoleGuard";
import api from "@/services/api";

interface FamilyMember {
  name: string;
  age?: number;
  relation?: string;
}

export default function FamilyMembersPage() {
  useRoleGuard(["user"]);
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [relation, setRelation] = useState("");
  const [message, setMessage] = useState("");
  const [familyMembers, setFamilyMembers] = useState<FamilyMember[]>([]);
  const [loading, setLoading] = useState(true);

  // Load family members from user profile
  useEffect(() => {
    loadFamilyMembers();
  }, []);

  const loadFamilyMembers = async () => {
    try {
      const { data } = await api.get("/user/profile");
      setFamilyMembers(data.familyMembers || []);
    } catch (err) {
      console.error("Failed to load family members:", err);
    } finally {
      setLoading(false);
    }
  };

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    
    // Debug: Check if token exists
    const token = localStorage.getItem("token");
    if (!token) {
      setMessage("❌ You are not logged in. Please login first.");
      setTimeout(() => {
        window.location.href = "/login";
      }, 2000);
      return;
    }
    
    try {
      await api.post("/user/family", { name, age: parseInt(age) || 0, relation });
      setMessage("✓ Family member added successfully!");
      setName("");
      setAge("");
      setRelation("");
      
      // Reload family members list
      loadFamilyMembers();
      
      // Clear message after 3 seconds
      setTimeout(() => setMessage(""), 3000);
    } catch (err: any) {
      const errorMsg = err?.response?.data?.message || err?.message || "Unable to add member.";
      setMessage(`❌ Error: ${errorMsg}`);
      console.error("Add family member error:", err?.response || err);
    }
  };

  return (
    <DashboardShell title="User Dashboard" nav={userNav}>
      <div className="max-w-5xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900">Manage Family Members</h1>
          <p className="mt-2 text-slate-600">Add family members to be covered under your insurance policies</p>
        </div>

        <form onSubmit={submit} className="bg-white rounded-xl border border-slate-200 shadow-sm mb-8">
          <div className="p-8">
            <h2 className="text-lg font-semibold text-slate-900 mb-6">Add New Family Member</h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Full Name <span className="text-red-500">*</span>
                </label>
                <input 
                  value={name} 
                  onChange={(e) => setName(e.target.value)} 
                  placeholder="e.g., Priya Kumar" 
                  required
                  className="w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Age <span className="text-red-500">*</span>
                </label>
                <input 
                  value={age} 
                  onChange={(e) => setAge(e.target.value)} 
                  type="number" 
                  placeholder="32" 
                  required
                  min="0"
                  max="120"
                  className="w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Relation <span className="text-red-500">*</span>
                </label>
                <input 
                  value={relation} 
                  onChange={(e) => setRelation(e.target.value)} 
                  placeholder="Spouse, Child, Parent" 
                  required
                  className="w-full"
                />
              </div>
            </div>
          </div>

          <div className="px-8 py-5 bg-slate-50 border-t border-slate-200 rounded-b-xl">
            {message && (
              <div className={`mb-4 p-4 rounded-lg text-sm border ${
                message.includes('✓') 
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
              Add Family Member
            </button>
          </div>
        </form>

        <div>
          <h2 className="text-xl font-semibold text-slate-900 mb-6">Family Members ({familyMembers.length})</h2>
          {loading ? (
            <div className="bg-white rounded-xl border border-slate-200 p-12 text-center">
              <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-cyan-600 border-r-transparent"></div>
              <p className="mt-4 text-slate-500">Loading family members...</p>
            </div>
          ) : familyMembers.length === 0 ? (
            <div className="bg-white rounded-xl border border-slate-200 p-12 text-center">
              <svg className="mx-auto h-12 w-12 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <p className="mt-4 text-slate-500">No family members added yet</p>
              <p className="mt-1 text-sm text-slate-400">Add family members using the form above</p>
            </div>
          ) : (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {familyMembers.map((member, index) => (
                <div key={index} className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-full bg-cyan-100 flex items-center justify-center flex-shrink-0">
                      <svg className="w-6 h-6 text-cyan-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-lg font-semibold text-slate-900 truncate">{member.name}</h3>
                      <div className="mt-2 space-y-1">
                        <p className="text-sm text-slate-600">
                          <span className="font-medium">Age:</span> {member.age || "N/A"} years
                        </p>
                        <p className="text-sm text-slate-600">
                          <span className="font-medium">Relation:</span> {member.relation || "N/A"}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </DashboardShell>
  );
}
