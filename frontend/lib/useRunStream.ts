"use client";
import { useEffect, useRef, useCallback } from "react";
import type { RunEvent, SubQuestion } from "./types";
import { runMock } from "./mock";

const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK !== "false";

export function useRunStream(runId: string, topic: string, onEvent: (e: RunEvent) => void) {
  const resolver = useRef<(o: SubQuestion[]) => void>(() => {});

  useEffect(() => {
    let dead = false;
    if (USE_MOCK) {
      const approval = new Promise<SubQuestion[]>((res) => (resolver.current = res));
      runMock(topic, onEvent, approval, () => dead);
      return () => { dead = true; };
    }
    const es = new EventSource(`/api/runs/${runId}/stream`);
    es.onmessage = (m) => onEvent(JSON.parse(m.data));
    es.onerror = () => es.close();
    return () => es.close();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [runId]);

  const approve = useCallback(async (outline: SubQuestion[]) => {
    if (USE_MOCK) return resolver.current(outline);
    await fetch(`/api/runs/${runId}/resume`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ outline }) });
  }, [runId]);

  return { approve };
}
