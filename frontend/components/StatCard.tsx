interface StatCardProps {
  label: string;
  value: string | number;
}

export default function StatCard({ label, value }: StatCardProps) {
  return (
    <div className="group bg-white rounded-xl p-6 shadow-sm border border-slate-200 hover:shadow-md hover:border-cyan-300 transition-all duration-200">
      <p className="text-sm font-medium text-slate-500 mb-2">{label}</p>
      <p className="text-3xl font-bold text-slate-900 group-hover:text-cyan-600 transition-colors">{value}</p>
    </div>
  );
}
