"use client";

import { useEffect, useMemo, useState } from "react";

import { apiGet, apiUploadPdf } from "@/lib/api";
import { Job, JobEvent, JobResult, RuntimeMetrics } from "@/lib/types";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [job, setJob] = useState<Job | null>(null);
  const [result, setResult] = useState<JobResult | null>(null);
  const [events, setEvents] = useState<JobEvent[]>([]);
  const [liveMetrics, setLiveMetrics] = useState<RuntimeMetrics | null>(null);
  const [liveMetricsUpdatedAt, setLiveMetricsUpdatedAt] = useState<string>("-");
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const canUpload = useMemo(() => !!file && !loading, [file, loading]);
  const latestMetrics = useMemo(() => {
    const withMetrics = [...events]
      .reverse()
      .find((event) =>
        ["cpu_pct", "ram_pct", "gpu_util_pct", "gpu_power_w"].some(
          (key) => event.event_payload[key as keyof typeof event.event_payload] !== undefined,
        ),
      );
    return withMetrics?.event_payload;
  }, [events]);

  const latestGpuMetrics = useMemo(() => {
    const withGpuMetrics = [...events]
      .reverse()
      .find((event) =>
        ["gpu_util_pct", "gpu_mem_util_pct", "gpu_power_w"].some((key) => {
          const value = event.event_payload[key as keyof typeof event.event_payload];
          return typeof value === "number" && !Number.isNaN(value);
        }),
      );
    return withGpuMetrics?.event_payload;
  }, [events]);

  const gpuDetected = useMemo(() => {
    return [latestGpuMetrics?.gpu_util_pct, latestGpuMetrics?.gpu_mem_util_pct, latestGpuMetrics?.gpu_power_w].some(
      (value) => typeof value === "number" && !Number.isNaN(value),
    );
  }, [latestGpuMetrics]);

  const metricsUpdatedAt = useMemo(() => {
    if (!events.length) return "-";
    const event = [...events].reverse().find((item) => item.created_at);
    return event?.created_at ? new Date(event.created_at).toLocaleTimeString() : "-";
  }, [events]);

  const metricNumber = (value: unknown, digits = 1) => {
    if (typeof value !== "number" || Number.isNaN(value)) return "-";
    return value.toFixed(digits);
  };

  const liveGpuDetected = useMemo(() => {
    return [liveMetrics?.gpu_util_pct, liveMetrics?.gpu_mem_util_pct, liveMetrics?.gpu_power_w].some(
      (value) => typeof value === "number" && !Number.isNaN(value),
    );
  }, [liveMetrics]);

  useEffect(() => {
    let cancelled = false;

    const pollRuntimeMetrics = async () => {
      try {
        const data = await apiGet<RuntimeMetrics>("/analytics/runtime/metrics");
        if (cancelled) return;
        setLiveMetrics(data);
        setLiveMetricsUpdatedAt(new Date().toLocaleTimeString());
      } catch {
        // Keep previous values when runtime endpoint is temporarily unavailable.
      }
    };

    pollRuntimeMetrics();
    const timer = setInterval(pollRuntimeMetrics, 2000);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, []);

  const pollJob = (jobId: string) => {
    const timer = setInterval(async () => {
      try {
        const [status, jobEvents] = await Promise.all([
          apiGet<Job>(`/jobs/${jobId}`),
          apiGet<JobEvent[]>(`/jobs/${jobId}/events?limit=200`),
        ]);
        setJob(status);
        setEvents(jobEvents);

        if (status.status === "completed" || status.status === "failed") {
          clearInterval(timer);
          const data = await apiGet<JobResult>(`/jobs/${jobId}/result`);
          setResult(data);
        }
      } catch (err) {
        clearInterval(timer);
        setError((err as Error).message);
      }
    }, 2500);
  };

  const onSubmit = async () => {
    if (!file) return;
    setLoading(true);
    setError("");
    setResult(null);
    setEvents([]);

    try {
      const uploaded = await apiUploadPdf(file);
      pollJob(uploaded.job_id);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-semibold">Subir nuevo paper</h2>
        <p className="muted">Analiza un PDF y estima su relacion con los 9 Planetary Boundaries.</p>
      </div>

      <section className="card space-y-4">
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="block w-full rounded-md border border-line bg-panelSoft p-3"
        />
        <button
          onClick={onSubmit}
          disabled={!canUpload}
          className="rounded-md bg-accent px-4 py-2 font-semibold text-black disabled:opacity-50"
        >
          {loading ? "Subiendo..." : "Procesar PDF"}
        </button>
      </section>

      <section className="card space-y-3">
        <h3 className="text-lg font-semibold">GPU en directo (servidor)</h3>
        <p className="muted text-sm">Actualizado: {liveMetricsUpdatedAt}</p>
        <p className="muted text-sm">GPU: {liveGpuDetected ? "detectada" : "sin datos disponibles"}</p>
        <div className="grid gap-2 md:grid-cols-3">
          <p><span className="muted">CPU:</span> {metricNumber(liveMetrics?.cpu_pct)}%</p>
          <p><span className="muted">RAM:</span> {metricNumber(liveMetrics?.ram_pct)}%</p>
          <p>
            <span className="muted">RAM usada:</span> {metricNumber(liveMetrics?.ram_used_mb, 0)} /
            {" "}{metricNumber(liveMetrics?.ram_total_mb, 0)} MB
          </p>
          <p><span className="muted">GPU uso:</span> {metricNumber(liveMetrics?.gpu_util_pct)}%</p>
          <p><span className="muted">GPU memoria:</span> {metricNumber(liveMetrics?.gpu_mem_util_pct)}%</p>
          <p><span className="muted">GPU potencia:</span> {metricNumber(liveMetrics?.gpu_power_w)} W</p>
        </div>
        <p className="muted text-xs">Estas metricas son del host y se actualizan aunque no subas ningun PDF.</p>
      </section>

      {job && (
        <section className="card space-y-2">
          <h3 className="text-lg font-semibold">Estado del job</h3>
          <p><span className="muted">Estado:</span> {job.status}</p>
          <p><span className="muted">Etapa:</span> {job.stage}</p>
          <p><span className="muted">Progreso:</span> {job.progress_pct}%</p>
          {job.error_message && <p className="text-red-400">{job.error_message}</p>}
        </section>
      )}

      {job && (
        <section className="card space-y-3">
          <h3 className="text-lg font-semibold">Metricas en directo (runtime)</h3>
          <p className="muted text-sm">Actualizado: {metricsUpdatedAt}</p>
          <p className="muted text-sm">GPU: {gpuDetected ? "detectada" : "sin datos en este job"}</p>
          <div className="grid gap-2 md:grid-cols-3">
            <p><span className="muted">CPU:</span> {metricNumber(latestMetrics?.cpu_pct)}%</p>
            <p><span className="muted">RAM:</span> {metricNumber(latestMetrics?.ram_pct)}%</p>
            <p>
              <span className="muted">RAM usada:</span> {metricNumber(latestMetrics?.ram_used_mb, 0)} /
              {" "}{metricNumber(latestMetrics?.ram_total_mb, 0)} MB
            </p>
            <p><span className="muted">GPU uso:</span> {metricNumber(latestGpuMetrics?.gpu_util_pct)}%</p>
            <p><span className="muted">GPU memoria:</span> {metricNumber(latestGpuMetrics?.gpu_mem_util_pct)}%</p>
            <p><span className="muted">GPU potencia:</span> {metricNumber(latestGpuMetrics?.gpu_power_w)} W</p>
          </div>
          <p className="muted text-xs">Si no hay GPU NVIDIA o no existe nvidia-smi, los campos de GPU aparecen en "-".</p>
        </section>
      )}

      {result?.pb_result && (
        <section className="card space-y-3">
          <h3 className="text-lg font-semibold">Resultado del analisis</h3>
          <p><span className="muted">Top PB:</span> {result.pb_result.top_pb_code}</p>
          <p><span className="muted">Score top:</span> {result.pb_result.top_pb_score.toFixed(4)}</p>
          <p><span className="muted">Resumen:</span> {result.summary}</p>
          <p><span className="muted">Abstract detectado:</span> {result.abstract_detected}</p>
          <p className="leading-7 text-textMain/90">{result.pb_result.explanation_text}</p>
        </section>
      )}

      {error && (
        <section className="card border-red-500/50">
          <p className="text-red-400">{error}</p>
        </section>
      )}
    </div>
  );
}
