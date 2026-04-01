import { Role } from "@/services/auth";

export default function RoleBadge({ role }: { role: Role }) {
  return (
    <span className="rounded-full border border-slate-300 bg-slate-100 px-2 py-1 text-xs font-medium uppercase text-slate-700">
      {role}
    </span>
  );
}
