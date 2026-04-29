PLAN_PROMPT = """
You are an expert research strategist.

Create a concise research plan for this topic:
Topic: {topic}
Report Type: {report_type}

Return:
1. A short research objective
2. 4 focused web search queries, each on a new line prefixed with '- '
3. The key dimensions to compare or analyze

Keep it practical and business-oriented.
"""

FINDINGS_PROMPT = """
You are an AI research analyst.

Topic: {topic}
Report Type: {report_type}

Below are web research snippets:
{search_context}

Summarize the most important findings as 6-10 bullet points.
Focus on factual, decision-useful insights.
Avoid repeating the same point.
"""

REPORT_PROMPT = """
You are a professional market intelligence analyst.

Write a polished report in markdown.

Topic: {topic}
Report Type: {report_type}

Research Findings:
{findings}

Sources:
{sources_text}

Structure the report with these sections:
# Title
## Executive Summary
## Key Findings
## Analysis
## Recommendations
## Sources

Make the report clear, professional, and recruiter-impressive.
"""
