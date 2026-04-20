import { apiGet } from "@/lib/api";
import { DistBarChart, DistLineChart, DistPieChart, KeywordBars } from "@/components/charts/analytics-charts";
import Link from "next/link";

import { DistributionResponse, KeywordItem, Overview, PaperListResponse } from "@/lib/types";

async function Kpis() {
  const data = await apiGet<Overview>("/analytics/overview");
  const items = [
    ["Papers totales", data.total_papers],
    ["Abstracts validos", data.abstracts_valid],
    ["Clasificados PB", data.papers_classified],
    ["Journals unicos", data.unique_journals],
    ["Longitud media abstract", Math.round(data.avg_abstract_length)],
  ];

  return (
    <section className="grid gap-4 md:grid-cols-3 lg:grid-cols-5">
      {items.map(([label, value]) => (
        <article key={label as string} className="card">
          <p className="muted text-sm">{label as string}</p>
          <p className="kpi-value">{value as number}</p>
        </article>
      ))}
    </section>
  );
}

async function DistCard({
  title,
  path,
  chart,
}: {
  title: string;
  path: string;
  chart: "bar" | "line" | "pie";
}) {
  const data = await apiGet<DistributionResponse>(path);
  const effectiveChart = path === "/analytics/distribution/year" && data.items.length <= 2 ? "bar" : chart;

  const chartNode =
    effectiveChart === "pie" ? (
      <DistPieChart data={data.items} />
    ) : effectiveChart === "line" ? (
      <DistLineChart data={data.items} />
    ) : (
      <DistBarChart data={data.items} />
    );

  return (
    <article className="card">
      <h3 className="mb-3 text-lg font-semibold">{title}</h3>
      {chartNode}
    </article>
  );
}

async function KeywordsCard() {
  const data = await apiGet<KeywordItem[]>("/analytics/keywords/global?limit=12");

  return (
    <article className="card lg:col-span-2">
      <h3 className="mb-3 text-lg font-semibold">Keywords mas frecuentes en UPV</h3>
      <KeywordBars data={data} />
    </article>
  );
}

async function PbFocusCard({ pbFocus }: { pbFocus: string | null }) {
  const pbDistribution = await apiGet<DistributionResponse>("/analytics/distribution/pb");
  const options = pbDistribution.items.map((item) => item.label).filter(Boolean);
  const activePb = pbFocus && options.includes(pbFocus) ? pbFocus : options[0] || "PB-UNK";
  const pbKeywords = await apiGet<KeywordItem[]>(`/analytics/keywords/pb/${encodeURIComponent(activePb)}?limit=12`);

  return (
    <article className="card lg:col-span-2 space-y-3">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h3 className="text-lg font-semibold">Foco por Planetary Boundary</h3>
          <p className="muted text-sm">Selecciona un PB para ver su perfil de keywords en UPV.</p>
        </div>
        <form className="flex items-center gap-2">
          <select
            name="pb_focus"
            defaultValue={activePb}
            className="rounded-md border border-line bg-panelSoft px-3 py-2 text-sm"
          >
            {options.map((pb) => (
              <option key={pb} value={pb}>
                {pb}
              </option>
            ))}
          </select>
          <button className="rounded-md bg-accent px-3 py-2 text-sm font-medium text-black">Ver</button>
        </form>
      </div>
      <KeywordBars data={pbKeywords} />
      <div>
        <Link href={`/papers?pb=${encodeURIComponent(activePb)}`} className="text-sm text-accent hover:underline">
          Explorar papers de {activePb}
        </Link>
      </div>
    </article>
  );
}

async function PapersQuickView() {
  const papers = await apiGet<PaperListResponse>("/papers?page=1&page_size=8&sort=year_desc&max_year=2024");

  return (
    <article className="card lg:col-span-2">
      <h3 className="mb-3 text-lg font-semibold">Papers recientes para analisis rapido</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="border-b border-line text-left text-textMuted">
              <th className="px-3 py-2">Paper</th>
              <th className="px-3 py-2">Anio</th>
              <th className="px-3 py-2">PB top</th>
              <th className="px-3 py-2">Accion</th>
            </tr>
          </thead>
          <tbody>
            {papers.items.map((paper) => (
              <tr key={paper.id} className="border-b border-line/60">
                <td className="px-3 py-3">{paper.title}</td>
                <td className="px-3 py-3">{paper.year ?? "-"}</td>
                <td className="px-3 py-3">{paper.pb_result?.top_pb_code ?? "N/A"}</td>
                <td className="px-3 py-3">
                  <Link href={`/papers/${paper.id}`} className="text-accent hover:underline">
                    Abrir analisis
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </article>
  );
}

export default async function DashboardPage({
  searchParams,
}: {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const params = await searchParams;
  const pbFocus = typeof params.pb_focus === "string" ? params.pb_focus : null;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-semibold">Corpus UPV</h2>
        <p className="muted">Panel analitico del corpus procesado y su cobertura PB.</p>
      </div>
      <Kpis />
      <section className="grid gap-4 lg:grid-cols-2">
        <DistCard title="Distribucion por Planetary Boundary" path="/analytics/distribution/pb" chart="pie" />
        <DistCard title="Publicaciones por anio" path="/analytics/distribution/year" chart="line" />
        <DistCard title="Longitud de abstracts" path="/analytics/distribution/abstract-length" chart="bar" />
        <KeywordsCard />
        <PbFocusCard pbFocus={pbFocus} />
        <PapersQuickView />
      </section>
    </div>
  );
}
