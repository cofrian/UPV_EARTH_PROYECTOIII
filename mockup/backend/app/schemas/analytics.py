from pydantic import BaseModel


class MetricItem(BaseModel):
    label: str
    value: int | float


class DashboardOverview(BaseModel):
    total_papers: int
    abstracts_valid: int
    papers_classified: int
    unique_journals: int
    avg_abstract_length: float


class DistributionResponse(BaseModel):
    items: list[MetricItem]


class KeywordItem(BaseModel):
    keyword: str
    value: int


class LengthComparison(BaseModel):
    paper_length: int
    global_avg_length: float
    pb_avg_length: float


class PaperKeywordComparison(BaseModel):
    paper_keywords: list[str]
    global_overlap: list[KeywordItem]
    pb_overlap: list[KeywordItem]
    global_top_keywords: list[KeywordItem]
    pb_top_keywords: list[KeywordItem]


class PaperComparisonResponse(BaseModel):
    paper_id: str
    title: str
    top_pb_code: str
    length_comparison: LengthComparison
    keyword_comparison: PaperKeywordComparison


class RuntimeMetricsResponse(BaseModel):
    cpu_pct: float
    ram_pct: float
    ram_used_mb: float
    ram_total_mb: float
    gpu_util_pct: float | None = None
    gpu_mem_util_pct: float | None = None
    gpu_power_w: float | None = None
