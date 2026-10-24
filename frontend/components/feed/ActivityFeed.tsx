"use client";
import { useEffect, useRef } from "react";
import { useRun } from "@/lib/store";

export default function ActivityFeed() {
  const feed = useRun((s) => s.feed);
  const end = useRef<HTMLDivElement>(null);
  useEffect(() => end.current?.scrollIntoView({ behavior: "smooth" }), [feed.length]);
  return (
    <div className="glass h-80 overflow-y-auto p-4" aria-live="polite">
      <h2 className="mb-3 text-sm font-semibold">Activity</h2>
      {feed.length === 0 && <p className="text-sm text-[var(--muted)]">Events appear here as agents work.</p>}
      <ul className="space-y-2 text-sm">
        {feed.map((f, i) => (
          <li key={i} className={f.includes("flagged") ? "text-amber-300" : "text-gray-300"}>{f}</li>
        ))}
      </ul>
      <div ref={end} />
    </div>
  );
}
