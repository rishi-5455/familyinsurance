"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

interface SidebarProps {
  items: { label: string; href: string }[];
  title: string;
}

export default function Sidebar({ items, title }: SidebarProps) {
  const pathname = usePathname();

  return (
    <aside className="w-full md:w-72 bg-white border-r border-slate-200 p-6 shadow-sm">
      <div className="mb-8">
        <h2 className="text-xl font-bold text-slate-900">{title}</h2>
        <div className="mt-2 h-1 w-12 bg-cyan-600 rounded-full"></div>
      </div>
      <nav className="space-y-1">
        {items.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`group flex items-center rounded-lg px-4 py-3 text-sm font-medium transition-all duration-150 ${
                active
                  ? "bg-cyan-600 text-white shadow-md"
                  : "text-slate-700 hover:bg-slate-100 hover:text-slate-900"
              }`}
            >
              {active && (
                <svg className="w-4 h-4 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              )}
              {!active && (
                <svg className="w-4 h-4 mr-3 text-slate-400 group-hover:text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              )}
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
