"""
Claude AI Executive Report Generator
Reads raw sales CSV data and uses Claude claude-sonnet-4-5 to generate a professional
executive summary report with business insights, margin analysis, and strategic recommendations.

Author: Sourojit Kar | github.com/Jeet908
Install: pip install anthropic pandas
"""

import os
import json
import anthropic
import pandas as pd
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================
CLAUDE_MODEL = "claude-sonnet-4-5"       # Best reasoning model for business analysis
DATA_PATH    = Path("sample_sales.csv")  # Your sales CSV file path


# ============================================================
# STEP 1: Load & Summarize Data
# ============================================================
def load_and_summarize(csv_path: Path) -> dict:
    """Loads CSV sales data and computes key summary statistics for Claude."""

    # If no CSV, generate sample data
    if not csv_path.exists():
        print("No CSV found — generating sample data...")
        sample = {
            "product":  ["Smart Monitor", "Task Chair", "Smartwatch", "Headphones", "USB Hub"],
            "category": ["Technology", "Office Supplies", "Consumer Electronics", "Technology", "Technology"],
            "region":   ["US-East", "US-West", "South Asia", "Central Europe", "East Asia"],
            "revenue":  [798.00, 260.00, 402.30, 338.30, 300.00],
            "cost":     [560.00, 140.00, 195.00, 220.00, 175.00],
            "quantity": [2, 1, 3, 2, 5],
            "discount": [0.05, 0.00, 0.10, 0.15, 0.00],
        }
        df = pd.DataFrame(sample)
        df.to_csv(csv_path, index=False)

    df = pd.read_csv(csv_path)
    df["profit"]     = df["revenue"] - df["cost"]
    df["margin_pct"] = (df["profit"] / df["revenue"] * 100).round(2)

    summary = {
        "total_transactions": len(df),
        "total_revenue":      round(df["revenue"].sum(), 2),
        "total_profit":       round(df["profit"].sum(), 2),
        "blended_margin_pct": round((df["profit"].sum() / df["revenue"].sum()) * 100, 2),
        "avg_order_value":    round(df["revenue"].mean(), 2),
        "revenue_by_category": df.groupby("category")["revenue"].sum().round(2).to_dict(),
        "revenue_by_region":  df.groupby("region")["revenue"].sum().round(2).to_dict(),
        "top_margin_product": df.loc[df["margin_pct"].idxmax(), "product"],
        "lowest_margin_product": df.loc[df["margin_pct"].idxmin(), "product"],
        "lowest_margin_pct":  df["margin_pct"].min(),
        "products": df[["product","category","region","revenue","profit","margin_pct"]].to_dict("records"),
    }
    return summary


# ============================================================
# STEP 2: Build Claude Prompt
# ============================================================
def build_prompt(summary: dict) -> str:
    return f"""You are a senior business intelligence analyst presenting to the C-suite.

Analyze the following retail sales performance data and produce a sharp, structured executive summary report.

=== SALES DATA SUMMARY ===
{json.dumps(summary, indent=2)}

=== REPORT REQUIREMENTS ===
Write a formal executive report with these exact sections:

1. EXECUTIVE OVERVIEW (2–3 sentences: highlight revenue, profit, and blended margin)
2. PERFORMANCE HIGHLIGHTS (2–3 bullet points: what is working well)
3. CRITICAL FINDINGS (2–3 bullet points: margin risks, underperforming categories or regions)
4. STRATEGIC RECOMMENDATIONS (3 numbered, actionable business interventions with projected impact)
5. CONCLUSION (1 sentence: projected financial improvement if recommendations are executed)

Tone: Professional, data-driven, C-suite ready. Use specific numbers from the data.
Format: Clean, structured plain text with clear section headers."""


# ============================================================
# STEP 3: Call Claude API & Stream Response
# ============================================================
def generate_report(summary: dict) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY environment variable not set.\n"
            "Get your key at https://console.anthropic.com/\n"
            "Then run: set ANTHROPIC_API_KEY=your_key_here (Windows)"
        )

    client = anthropic.Anthropic(api_key=api_key)
    prompt = build_prompt(summary)

    print("\n🤖 Generating executive report via Claude claude-sonnet-4-5...\n")
    print("=" * 60)

    full_response = ""
    with client.messages.stream(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_response += text

    print("\n" + "=" * 60)
    return full_response


# ============================================================
# MAIN PIPELINE
# ============================================================
if __name__ == "__main__":
    print("📊 Claude AI Executive Report Generator")
    print("Loading and summarizing sales data...")

    summary = load_and_summarize(DATA_PATH)

    print(f"\n✅ Data loaded: {summary['total_transactions']} transactions")
    print(f"   Total Revenue:  ${summary['total_revenue']:,.2f}")
    print(f"   Total Profit:   ${summary['total_profit']:,.2f}")
    print(f"   Blended Margin: {summary['blended_margin_pct']}%")

    report = generate_report(summary)

    # Save report to file
    output_path = Path("executive_report.txt")
    output_path.write_text(report, encoding="utf-8")
    print(f"\n✅ Report saved to {output_path}")
