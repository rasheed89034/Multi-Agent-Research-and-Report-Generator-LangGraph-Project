import Link from "next/link";

const runs = [
  { id: "a1b2c3d4", topic: "Solid-state batteries in 2026", status: "completed", cost: "$0.42", time: "3m 12s" },
  { id: "e5f6a7b8", topic: "How retrieval-augmented generation fails", status: "paused", cost: "$0.18", time: "1m 05s" },
  { id: "c9d0e1f2", topic: "Sodium-ion vs lithium-ion costs", status: "running", cost: "$0.09", time: "0m 40s" },
];
const tone: Record<string, string> = { completed: "text-emerald-300", paused: "text-amber-300", running: "text-indigo-300" };

export default function History() {
  return (
    <div className="mx-auto max-w-4xl">
      <h1 className="mb-4 text-2xl font-semibold">Past research</h1>
      <div className="space-y-2">
        {runs.map((r) => (
          <Link key={r.id} href={`/runs/${r.id}?topic=${encodeURIComponent(r.topic)}`} className="glass flex items-center justify-between gap-4 p-4 hover:border-indigo-400/50">
            <span className="font-medium">{r.topic}</span>
            <span className="flex gap-4 text-sm text-[var(--muted)]"><span className={tone[r.status]}>{r.status}</span><span>{r.cost}</span><span>{r.time}</span></span>
          </Link>
        ))}
      </div>
    </div>
  );
}
