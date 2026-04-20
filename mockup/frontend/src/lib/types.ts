export type MetricItem = {
  label: string;
  value: number;
};

export type Overview = {
  total_papers: number;
  abstracts_valid: number;
  papers_classified: number;
  unique_journals: number;
  avg_abstract_length: number;
};

export type PBResult = {
  top_pb_code: string;
  top_pb_score: number;
  secondary_pbs: Array<{ pb_code: string; pb_name?: string; score: number }> | Record<string, unknown>;
  score_map: Record<string, number>;
  explanation_text: string;
};

export type Paper = {
  id: string;
  doc_id: string | null;
  title: string;
  abstract_norm: string;
  year: number | null;
  doi: string | null;
  source: string | null;
  journal: string | null;
  keywords: string | null;
  pb_result: PBResult | null;
};

export type PaperListResponse = {
  total: number;
  page: number;
  page_size: number;
  items: Paper[];
};

export type DistributionResponse = {
  items: MetricItem[];
};

export type KeywordItem = {
  keyword: string;
  value: number;
};

export type LengthComparison = {
  paper_length: number;
  global_avg_length: number;
  pb_avg_length: number;
};

export type PaperKeywordComparison = {
  paper_keywords: string[];
  global_overlap: KeywordItem[];
  pb_overlap: KeywordItem[];
  global_top_keywords: KeywordItem[];
  pb_top_keywords: KeywordItem[];
};

export type PaperComparison = {
  paper_id: string;
  title: string;
  top_pb_code: string;
  length_comparison: LengthComparison;
  keyword_comparison: PaperKeywordComparison;
};

export type Job = {
  id: string;
  paper_id: string | null;
  filename_original: string;
  status: string;
  stage: string;
  progress_pct: number;
  error_code: string | null;
  error_message: string | null;
};

export type JobResult = {
  job: Job;
  abstract_detected: string | null;
  summary: string | null;
  pb_result: PBResult | null;
};

export type RuntimeMetrics = {
  cpu_pct?: number | null;
  ram_pct?: number | null;
  ram_used_mb?: number | null;
  ram_total_mb?: number | null;
  gpu_util_pct?: number | null;
  gpu_mem_util_pct?: number | null;
  gpu_power_w?: number | null;
};

export type JobEvent = {
  id: string;
  job_id: string;
  event_type: string;
  event_payload: Record<string, unknown> & RuntimeMetrics;
  created_at: string | null;
};
