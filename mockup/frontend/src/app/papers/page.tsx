import Link from "next/link";

import { apiGet } from "@/lib/api";
import { PaperListResponse } from "@/lib/types";

const HIDDEN_DOC_IDS = new Set(["b39624d6c38a"]);
const HIDDEN_TITLE_PATTERNS = ["chapter 34 the role of hydrological modelling uncertainties"];

function isHiddenPaper(docId: string | null, title: string): boolean {
  const docKey = (docId || "").trim().toLowerCase();
  const titleKey = (title || "").trim().toLowerCase();
  if (HIDDEN_DOC_IDS.has(docKey)) return true;
  return HIDDEN_TITLE_PATTERNS.some((pattern) => titleKey.includes(pattern));
}

export default async function PapersPage({ searchParams }: { searchParams: Promise<Record<string, string | string[] | undefined>> }) {
  const params = await searchParams;
  const query = typeof params.query === "string" ? params.query : "";
  const year = typeof params.year === "string" ? params.year : "";
  const pb = typeof params.pb === "string" ? params.pb : "";
  const page = typeof params.page === "string" ? params.page : "1";

  const qs = new URLSearchParams();
  if (query) qs.set("query", query);
  if (year) qs.set("year", year);
  if (pb) qs.set("pb", pb);
  qs.set("page", page);
  qs.set("page_size", "20");

  const data = await apiGet<PaperListResponse>(`/papers?${qs.toString()}`);
  const visibleItems = data.items.filter((paper) => !isHiddenPaper(paper.doc_id, paper.title));
  const hiddenInPage = data.items.length - visibleItems.length;
  const visibleTotal = Math.max(0, data.total - hiddenInPage);

  return (
    <div className="space-y-5">
      <div>
        <h2 className="text-3xl font-semibold">Exploracion de papers</h2>
        <p className="muted">Busqueda y filtros sobre el corpus ya analizado.</p>
      </div>

      <form className="card grid gap-3 md:grid-cols-4">
        <input name="query" defaultValue={query} placeholder="Buscar titulo/abstract" className="rounded-md border border-line bg-panelSoft px-3 py-2" />
        <input name="year" defaultValue={year} placeholder="Anio" className="rounded-md border border-line bg-panelSoft px-3 py-2" />
        <input name="pb" defaultValue={pb} placeholder="PB code (ej. PB1)" className="rounded-md border border-line bg-panelSoft px-3 py-2" />
        <button className="rounded-md bg-accent px-3 py-2 font-medium text-black">Aplicar filtros</button>
      </form>

      <section className="card overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="border-b border-line text-left text-textMuted">
              <th className="px-3 py-2">Titulo</th>
              <th className="px-3 py-2">Anio</th>
              <th className="px-3 py-2">Journal</th>
              <th className="px-3 py-2">PB top</th>
              <th className="px-3 py-2">Detalle</th>
            </tr>
          </thead>
          <tbody>
            {visibleItems.map((paper) => (
              <tr key={paper.id} className="border-b border-line/60">
                <td className="px-3 py-3">{paper.title}</td>
                <td className="px-3 py-3">{paper.year ?? "-"}</td>
                <td className="px-3 py-3">{paper.journal ?? "-"}</td>
                <td className="px-3 py-3">{paper.pb_result?.top_pb_code ?? "N/A"}</td>
                <td className="px-3 py-3">
                  <Link href={`/papers/${paper.id}`} className="text-accent hover:underline">
                    Ver
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <p className="muted">Total resultados: {visibleTotal}</p>
    </div>
  );
}
