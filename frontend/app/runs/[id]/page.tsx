"use client";
import { Suspense, useEffect, useState } from "react";
import { useParams, useSearchParams } from "next/navigation";
import AgentGraph from "@/components/graph/AgentGraph";
import ActivityFeed from "@/components/feed/ActivityFeed";
import SourceCard from "@/components/evidence/SourceCard";
import OutlineEditor from "@/components/outline/OutlineEditor";
import ReportView from "@/components/report/ReportView";
import { useRun } from "@/lib/store";
import { useRunStream } from "@/lib/useRunStream";

function Run() {
  const { id } = useParams<{ id: string }>();
  const topic = useSearchParams().get("topic") ?? "Untitled research";
  const { apply, reset, awaiting, outline, findings, report, sources, done, error } = useRun();
  const [tab, setTab] = useState<"live" | "report">("live");
  useEffect(() => { reset(); }, [id, reset]);
  const { approve } = useRunStream(id, topic, apply);
  useEffect(() => { if (done && report) setTab("report"); }, [done, report]);

  return (
    <div className="mx-auto max-w-6xl space-y-4">
      <header className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-semibold">{topic}</h1>
        <div className="glass flex p-1 text-sm">
          {(["live", "report"] as const).map((t) => (
            <button key={t} disabled={t === "report" && !report} onClick={() => setTab(t)}
              className={`rounded-xl px-4 py-1.5 disabled:opacity-40 ${tab === t ? "bg-indigo-500/30" : ""}`}>{t === "live" ? "Live run" : "Report"}</button>
          ))}
        </div>
      </header>

      {error && (
        <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-300">
          <div className="font-semibold text-red-200">Execution Error</div>
          <p className="mt-1">{error}</p>
        </div>
      )}

      {tab === "report" ? <ReportView markdown={report} sources={sources} /> : awaiting ? (
        <OutlineEditor initial={outline} onApprove={(o) => { useRun.setState({ awaiting: false, outline: o }); approve(o); }} />
      ) : (
        <>
          <div className="grid gap-4 lg:grid-cols-[2fr_1fr]"><AgentGraph /><ActivityFeed /></div>
          <section>
            <h2 className="mb-3 text-sm font-semibold">Evidence ({findings.length})</h2>
            {findings.length === 0 && <p className="text-sm text-[var(--muted)]">Sources will appear once researchers start.</p>}
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{findings.map((f, i) => <SourceCard key={i} f={f} />)}</div>
          </section>
        </>
      )}
    </div>
  );
}

export default function Page() { return <Suspense><Run /></Suspense>; }
