from typing import List, TypedDict


class ResearchState(TypedDict):
    topic: str
    report_type: str
    max_results: int
    research_plan: str
    search_queries: List[str]
    raw_search_results: List[dict]
    findings: List[str]
    final_report: str
    sources: List[dict]
