from langgraph.graph import END, StateGraph

from src.models import get_llm, get_tavily_client
from src.prompts import FINDINGS_PROMPT, PLAN_PROMPT, REPORT_PROMPT
from src.state import ResearchState
from src.utils import dedupe_sources, extract_queries_from_plan


def plan_research(state: ResearchState) -> ResearchState:
    llm = get_llm()
    prompt = PLAN_PROMPT.format(
        topic=state["topic"],
        report_type=state["report_type"],
    )
    response = llm.invoke(prompt)
    plan_text = response.content.strip()
    queries = extract_queries_from_plan(plan_text)

    return {
        **state,
        "research_plan": plan_text,
        "search_queries": queries,
    }


def search_web(state: ResearchState) -> ResearchState:
    client = get_tavily_client()
    all_results = []

    for query in state["search_queries"]:
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=state["max_results"],
        )
        results = response.get("results", [])
        all_results.extend(results)

    return {
        **state,
        "raw_search_results": all_results,
        "sources": dedupe_sources(all_results),
    }


def summarize_findings(state: ResearchState) -> ResearchState:
    llm = get_llm()

    snippets = []
    for item in state["raw_search_results"][:12]:
        title = item.get("title", "Untitled")
        content = item.get("content", "")
        url = item.get("url", "")
        snippets.append(f"Title: {title}\nURL: {url}\nSnippet: {content}")

    search_context = "\n\n".join(snippets)

    prompt = FINDINGS_PROMPT.format(
        topic=state["topic"],
        report_type=state["report_type"],
        search_context=search_context,
    )
    response = llm.invoke(prompt)
    findings_text = response.content.strip()

    findings = [
        line.strip("- ").strip()
        for line in findings_text.splitlines()
        if line.strip()
    ]

    return {
        **state,
        "findings": findings,
    }


def generate_report(state: ResearchState) -> ResearchState:
    llm = get_llm()

    findings_text = "\n".join([f"- {item}" for item in state["findings"]])
    sources_text = "\n".join(
        [f"- {src['title']}: {src['url']}" for src in state["sources"]]
    )

    prompt = REPORT_PROMPT.format(
        topic=state["topic"],
        report_type=state["report_type"],
        findings=findings_text,
        sources_text=sources_text,
    )
    response = llm.invoke(prompt)

    return {
        **state,
        "final_report": response.content.strip(),
    }


def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("plan_research", plan_research)
    graph.add_node("search_web", search_web)
    graph.add_node("summarize_findings", summarize_findings)
    graph.add_node("generate_report", generate_report)

    graph.set_entry_point("plan_research")
    graph.add_edge("plan_research", "search_web")
    graph.add_edge("search_web", "summarize_findings")
    graph.add_edge("summarize_findings", "generate_report")
    graph.add_edge("generate_report", END)

    return graph.compile()


def run_research_graph(topic: str, report_type: str, max_results: int = 5) -> ResearchState:
    app = build_graph()

    initial_state: ResearchState = {
        "topic": topic,
        "report_type": report_type,
        "max_results": max_results,
        "research_plan": "",
        "search_queries": [],
        "raw_search_results": [],
        "findings": [],
        "final_report": "",
        "sources": [],
    }

    return app.invoke(initial_state)
