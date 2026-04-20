import { apiGet } from "@/lib/api";
import { KeywordBars, LengthComparisonChart } from "@/components/charts/analytics-charts";
import { Paper, PaperComparison } from "@/lib/types";

export default async function PaperDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const paper = await apiGet<Paper>(`/papers/${id}`);
  const comparison = await apiGet<PaperComparison>(`/analytics/papers/${id}/comparison`);

  return (
    <div className="space-y-5">
      <div>
        <h2 className="text-2xl font-semibold">{paper.title}</h2>
        <p className="muted">{paper.journal || "Journal no disponible"} · {paper.year || "-"}</p>
      </div>

      <article className="card space-y-3">
        <h3 className="text-lg font-semibold">Abstract</h3>
        <p className="leading-7 text-textMain/90">{paper.abstract_norm}</p>
      </article>

      <article className="card space-y-3">
        <h3 className="text-lg font-semibold">Resultado Planetary Boundaries</h3>
        <p><span className="muted">Top PB:</span> {paper.pb_result?.top_pb_code ?? "N/A"}</p>
        <p><span className="muted">Score:</span> {paper.pb_result?.top_pb_score?.toFixed(4) ?? "N/A"}</p>
        <p className="leading-7 text-textMain/90">{paper.pb_result?.explanation_text ?? "Sin explicacion disponible"}</p>
      </article>

      <article className="card space-y-3">
        <h3 className="text-lg font-semibold">Comparativa de longitud del abstract</h3>
        <p className="muted">Paper vs media global UPV y media del mismo PB ({comparison.top_pb_code}).</p>
        <LengthComparisonChart
          paperLength={comparison.length_comparison.paper_length}
          globalAvg={comparison.length_comparison.global_avg_length}
          pbAvg={comparison.length_comparison.pb_avg_length}
        />
      </article>

      <section className="grid gap-4 lg:grid-cols-2">
        <article className="card space-y-3">
          <h3 className="text-lg font-semibold">Overlap de keywords con corpus global</h3>
          <KeywordBars data={comparison.keyword_comparison.global_overlap} />
        </article>

        <article className="card space-y-3">
          <h3 className="text-lg font-semibold">Overlap de keywords con su PB</h3>
          <KeywordBars data={comparison.keyword_comparison.pb_overlap} />
        </article>

        <article className="card space-y-3">
          <h3 className="text-lg font-semibold">Top keywords globales</h3>
          <KeywordBars data={comparison.keyword_comparison.global_top_keywords} />
        </article>

        <article className="card space-y-3">
          <h3 className="text-lg font-semibold">Top keywords en {comparison.top_pb_code}</h3>
          <KeywordBars data={comparison.keyword_comparison.pb_top_keywords} />
        </article>
      </section>

      <article className="card space-y-3">
        <h3 className="text-lg font-semibold">Keywords del paper</h3>
        <div className="flex flex-wrap gap-2">
          {comparison.keyword_comparison.paper_keywords.length === 0 ? (
            <p className="muted">No hay keywords estructuradas para este paper.</p>
          ) : (
            comparison.keyword_comparison.paper_keywords.map((keyword) => (
              <span key={keyword} className="rounded-full border border-line bg-panelSoft px-3 py-1 text-sm text-textMain/90">
                {keyword}
              </span>
            ))
          )}
        </div>
      </article>
    </div>
  );
}
