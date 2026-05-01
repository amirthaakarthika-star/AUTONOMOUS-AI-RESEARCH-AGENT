# Autonomous AI Research Agent

An AI-powered research assistant that turns a topic into a structured, source-backed report. The app uses LangGraph to run a multi-step research workflow: plan the research, search the web, summarize findings, and generate a polished markdown report with downloadable PDF output.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](#tech-stack)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red)](#run-the-app)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agent_Workflow-purple)](#how-it-works)
[![Groq](https://img.shields.io/badge/Groq-LLM_API-orange)](#environment-variables)
[![Tavily](https://img.shields.io/badge/Tavily-Web_Search-green)](#environment-variables)

## Overview

This project is built for fast research tasks such as competitor analysis, market research, and trend reports. Instead of manually opening many tabs, collecting notes, and writing a report from scratch, the agent runs an autonomous workflow and produces a clean research document.

The Streamlit interface lets users choose a report type, enter a research topic, control the number of web search results, inspect the research plan, review findings, and download the final report as a PDF.

## Key Features

| Feature | Description |
| --- | --- |
| Research planning | Creates a focused research objective and search strategy from the user topic |
| Live web search | Uses Tavily to collect current source-backed information |
| Multi-step agent workflow | Uses LangGraph to organize planning, search, summarization, and report generation |
| AI-written report | Uses Groq LLMs to generate a professional markdown research report |
| Source tracking | Displays source links used during the research process |
| PDF export | Converts the generated report into a downloadable PDF |
| Streamlit UI | Provides a simple, interactive interface for running research |

## Tech Stack

| Technology | Purpose |
| --- | --- |
| Python | Core application language |
| Streamlit | Web app interface |
| LangGraph | Agent workflow orchestration |
| LangChain | LLM integration utilities |
| Groq API | LLM-powered planning, summarization, and report writing |
| Tavily API | Live web search |
| ReportLab | PDF report generation |
| python-dotenv | Local environment variable management |

## How It Works

```text
User Topic
   |
   v
Research Planner
   |
   v
Live Web Search
   |
   v
Findings Summarizer
   |
   v
Markdown Report Generator
   |
   v
PDF Download
```

## Project Structure

```text
AUTONOMOUS-AI-RESEARCH-AGENT/
+-- app.py                    # Streamlit app and UI logic
+-- requirements.txt          # Python dependencies
+-- README.md                 # Project documentation
+-- src/
    +-- graph.py              # LangGraph workflow
    +-- models.py             # Groq and Tavily client setup
    +-- prompts.py            # Research, findings, and report prompts
    +-- report_generator.py   # Markdown and PDF export helpers
    +-- state.py              # Research state definition
    +-- utils.py              # Utility functions
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/amirthaakarthika-star/AUTONOMOUS-AI-RESEARCH-AGENT.git
cd AUTONOMOUS-AI-RESEARCH-AGENT
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Keep `.env` private. It should not be committed to GitHub.

## Run the App

Start the Streamlit app:

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in your terminal, usually:

```text
http://localhost:8501
```

## Example Research Topics

- Compare the top AI interview preparation platforms for students.
- Analyze current trends in autonomous AI agents for business research.
- Research competitors in the no-code website builder market.
- Study the growth of AI tools in education technology.

## Output

The app generates a report with sections such as:

- Executive Summary
- Key Findings
- Analysis
- Recommendations
- Sources

Reports can be reviewed inside the app and downloaded as a PDF.

## Notes

- This project is designed as a local AI research assistant and portfolio project.
- Search quality depends on the topic, Tavily results, and the number of search results selected.
- For production use, consider adding authentication, persistent storage, report history, and stronger source validation.

## License

This project is for learning, experimentation, and portfolio use.
