import type { Source } from "@/lib/types";

export default function CitationChip({ n, source }: { n: number; source?: Source }) {
  return (
    <span className="group relative mx-0.5 inline-block align-baseline">
      <a href={source?.url} target="_blank" rel="noreferrer" className="rounded bg-indigo-500/20 px-1.5 text-xs text-indigo-200 hover:bg-indigo-500/40">{n}</a>
      {source && (
        <span className="glass pointer-events-none absolute bottom-full left-0 z-10 mb-2 hidden w-64 p-3 text-xs group-hover:block group-focus-within:block">
          <b className="block">{source.domain}</b>
          <i className="text-[var(--muted)]">{source.snippet}</i>
        </span>
      )}
    </span>
  );
}
