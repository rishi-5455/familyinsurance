"use client";

import { useEffect, useState } from "react";
import DashboardShell from "@/components/DashboardShell";
import RoleBadge from "@/components/RoleBadge";
import { userNav } from "@/components/dashboardNav";
import { useRoleGuard } from "@/hooks/useRoleGuard";
import api from "@/services/api";
import { connectPeraWallet } from "@/services/wallet";

export default function UserProfilePage() {
  useRoleGuard(["user"]);
  const [profile, setProfile] = useState<any>(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    api.get("/user/profile").then((res) => setProfile(res.data)).catch(() => setProfile(null));
  }, []);

  const linkWallet = async () => {
    const account = await connectPeraWallet();
    if (!account) {
      setMessage("Wallet connection failed");
      return;
    }
    await api.post("/user/link-wallet", { walletAddress: account });
    setProfile((prev: any) => ({ ...prev, walletAddress: account }));
    setMessage("Wallet linked successfully");
  };

  return (
    <DashboardShell title="User Dashboard" nav={userNav}>
      <h1 className="text-2xl font-semibold">Profile</h1>
      {profile && (
        <div className="mt-6 max-w-xl rounded-xl bg-white p-6 border border-slate-200 space-y-2">
          <p><strong>Name:</strong> {profile.name}</p>
          <p><strong>Email:</strong> {profile.email}</p>
          <p><strong>Wallet:</strong> {profile.walletAddress || "Not linked"}</p>
          <button onClick={linkWallet} className="bg-brand-700 text-white">Link Pera Wallet</button>
          {message && <p className="text-sm">{message}</p>}
          <RoleBadge role={profile.role} />
        </div>
      )}
    </DashboardShell>
  );
}
