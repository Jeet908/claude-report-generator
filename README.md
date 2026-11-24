# 🤖 Claude AI Executive Report Generator

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Claude API](https://img.shields.io/badge/Claude-claude--sonnet--4--5-orange?logo=anthropic)](https://anthropic.com)

An AI-powered Python application that reads raw retail sales CSV data and uses **Anthropic's Claude claude-sonnet-4-5 API** to automatically generate a structured, C-suite-ready executive performance report with strategic business recommendations.

---

## 📌 Business Problem
Finance and operations teams spend hours manually writing weekly/monthly executive summaries from raw data. This tool automates that process — feeding structured sales metrics directly to Claude to produce a professional executive report in seconds.

## 🏗️ Pipeline Architecture
```
CSV Sales Data
     ↓
Pandas Data Summary (revenue, profit, margin, regional breakdown)
     ↓
Claude claude-sonnet-4-5 API (Streamed prompt → structured report generation)
     ↓
Executive Report Output (console + saved to executive_report.txt)
```

## 🤖 Claude API Concepts Demonstrated
- **Messages API** with structured system context
- **Streaming responses** (`stream.text_stream`) for real-time output
- **Business-domain prompt engineering** for structured report generation
- **Secure API key handling** via environment variables

## 🚀 Setup & Run
```bash
pip install anthropic pandas

# Set your API key
set ANTHROPIC_API_KEY=your_key_here    # Windows
export ANTHROPIC_API_KEY=your_key_here # Mac/Linux

python generate_report.py
```

## 📊 Sample Output
```
1. EXECUTIVE OVERVIEW
Total net revenue reached $2,098.60 across 5 product lines with a blended
profit margin of 42.7%, indicating healthy overall operational efficiency...

4. STRATEGIC RECOMMENDATIONS
1. Cap peripheral discounts to 5% maximum to recover $115k in annual margin.
2. Reallocate buffer inventory from EU to US-West to capture $170k in demand...
```

## 👤 Author
**Sourojit Kar** | [github.com/Jeet908](https://github.com/Jeet908)
