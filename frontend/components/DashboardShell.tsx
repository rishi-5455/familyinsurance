"use client";

import { ReactNode } from "react";
import Sidebar from "@/components/Sidebar";

interface DashboardShellProps {
  title: string;
  nav: { label: string; href: string }[];
  children: ReactNode;
}

export default function DashboardShell({ title, nav, children }: DashboardShellProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-cyan-50 via-slate-50 to-emerald-50">
      <div className="mx-auto max-w-7xl md:flex">
        <Sidebar items={nav} title={title} />
        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  );
}
