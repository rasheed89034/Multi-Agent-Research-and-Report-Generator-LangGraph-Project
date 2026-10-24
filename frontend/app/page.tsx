"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { Search } from "lucide-react";

const depths = ["Quick", "Standard", "Deep"];
const examples = ["Solid-state batteries in 2026", "How retrieval-augmented generation fails", "Sodium-ion vs lithium-ion costs"];

export default function Home() {
  const [topic, setTopic] = useState("");
  const [depth, setDepth] = useState("Standard");
  const router = useRouter();
  const start = (t = topic) => {
    if (!t.trim()) return;
    router.push(`/runs/${crypto.randomUUID().slice(0, 8)}?topic=${encodeURIComponent(t)}&depth=${depth}`);
  };
  return (
    <div className="mx-auto mt-[12vh] max-w-2xl">
      <h1 className="text-4xl font-semibold tracking-tight">What should the team research?</h1>
      <p className="mt-3 text-[var(--muted)]">A planner, parallel researchers, a critic and a writer will build a cited report. You approve the outline first.</p>
      <div className="glass mt-8 flex items-center gap-3 p-3">
        <Search className="ml-2 text-[var(--muted)]" size={18} />
        <input value={topic} onChange={(e) => setTopic(e.target.value)} onKeyDown={(e) => e.key === "Enter" && start()}
          placeholder="Describe a topic or question" className="flex-1 bg-transparent py-2 outline-none" />
        <button className="btn" onClick={() => start()} disabled={!topic.trim()}>Start research</button>
      </div>
      <div className="mt-4 flex items-center gap-2 text-sm">
        <span className="text-[var(--muted)]">Depth</span>
        {depths.map((d) => (
          <button key={d} onClick={() => setDepth(d)} className={`rounded-full border px-3 py-1 ${depth === d ? "border-indigo-400 bg-indigo-500/20" : "border-white/10 hover:bg-white/5"}`}>{d}</button>
        ))}
      </div>
      <div className="mt-8 flex flex-wrap gap-2">
        {examples.map((e) => (
          <button key={e} onClick={() => { setTopic(e); start(e); }} className="glass px-3 py-1.5 text-sm text-[var(--muted)] hover:text-white">{e}</button>
        ))}
      </div>
    </div>
  );
}
