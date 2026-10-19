import CitationChip from "./CitationChip";
import type { Source } from "@/lib/types";

function withCitations(text: string, sources: Source[]) {
  return text.split(/(\[\d+\])/g).map((part, i) => {
    const m = part.match(/^\[(\d+)\]$/);
    return m ? <CitationChip key={i} n={+m[1]} source={sources[+m[1] - 1]} /> : <span key={i}>{part}</span>;
  });
}

export default function ReportView({ markdown, sources }: { markdown: string; sources: Source[] }) {
  const copy = () => navigator.clipboard.writeText(markdown);
  return (
    <article className="glass mx-auto max-w-3xl p-8">
      <div className="mb-4 flex justify-end gap-2 text-sm">
        <button onClick={copy} className="rounded-lg border border-white/10 px-3 py-1 hover:bg-white/5">Copy markdown</button>
        <button onClick={() => window.print()} className="rounded-lg border border-white/10 px-3 py-1 hover:bg-white/5">Print or save PDF</button>
      </div>
      {markdown.split("\n").filter(Boolean).map((line, i) =>
        line.startsWith("# ") ? <h1 key={i} className="mb-4 text-3xl font-semibold">{line.slice(2)}</h1>
        : line.startsWith("## ") ? <h2 key={i} className="mb-2 mt-6 text-xl font-semibold">{line.slice(3)}</h2>
        : <p key={i} className="leading-7 text-gray-300">{withCitations(line, sources)}</p>)}
      <h2 className="mb-2 mt-8 text-lg font-semibold">Sources</h2>
      <ol className="list-decimal space-y-1 pl-5 text-sm text-[var(--muted)]">
        {sources.map((s, i) => <li key={i}><a href={s.url} className="hover:text-white" target="_blank" rel="noreferrer">{s.domain}</a></li>)}
      </ol>
    </article>
  );
}
