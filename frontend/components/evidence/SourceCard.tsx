import type { Finding } from "@/lib/types";

const tone = { high: "bg-emerald-500/15 text-emerald-300", medium: "bg-amber-500/15 text-amber-300", low: "bg-rose-500/15 text-rose-300" };

export default function SourceCard({ f }: { f: Finding }) {
  return (
    <a href={f.source.url} target="_blank" rel="noreferrer" className="glass block p-3 text-sm hover:border-indigo-400/50">
      <div className="flex items-center gap-2">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={`https://www.google.com/s2/favicons?domain=${f.source.domain}&sz=32`} alt="" width={16} height={16} />
        <span className="flex-1 truncate text-[var(--muted)]">{f.source.domain}</span>
        <span className={`rounded-full px-2 py-0.5 text-xs ${tone[f.confidence]}`}>{f.confidence} confidence</span>
      </div>
      <p className="mt-2">{f.claim}</p>
      <p className="mt-1 line-clamp-2 text-xs italic text-[var(--muted)]">{f.source.snippet}</p>
    </a>
  );
}
