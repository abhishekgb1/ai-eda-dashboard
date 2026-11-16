"""Export a real, interactive Plotly dashboard as a standalone HTML file."""

from __future__ import annotations

from html import escape
from typing import Any

from plotly.io import to_html


def build_interactive_dashboard_html(
    filename: str,
    kpi_results: list[dict[str, Any]],
    chart_figures: list[tuple[Any, str]],
    insights: list[str],
) -> str:
    """Create a responsive HTML dashboard with interactive Plotly charts."""
    metric_cards = []
    for item in kpi_results:
        name = escape(str(item.get("name", "Metric")))
        value = escape(str(item.get("formatted", "—")))
        aggregation = escape(str(item.get("agg", "")).upper())
        column = escape(str(item.get("column", "")))
        delta = item.get("delta")
        delta_text = f"{float(delta):+.1f}% · {escape(str(item.get('delta_label', '')))}" if delta is not None else ""
        metric_cards.append(
            f'<article class="metric"><p class="metric-label">{name}</p>'
            f'<p class="metric-value">{value}</p>'
            f'<p class="metric-detail">{aggregation} {column}</p>'
            f'<p class="metric-delta">{delta_text}</p></article>'
        )

    chart_sections = []
    for index, (figure, description) in enumerate(chart_figures):
        chart = to_html(
            figure,
            full_html=False,
            include_plotlyjs=True if index == 0 else False,
            config={"responsive": True, "displaylogo": False},
        )
        caption = f'<p class="caption">{escape(str(description))}</p>' if description else ""
        chart_sections.append(f'<section class="panel">{caption}{chart}</section>')

    insight_items = "".join(f"<li>{escape(str(item))}</li>" for item in insights)
    insight_section = (
        f'<section class="panel"><h2>Key insights</h2><ul>{insight_items}</ul></section>'
        if insight_items
        else ""
    )
    cards_html = "".join(metric_cards) or '<p class="empty">No KPIs were generated.</p>'
    charts_html = "".join(chart_sections) or '<p class="empty">No charts were generated.</p>'
    title = escape(str(filename))

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Interactive EDA Dashboard · {title}</title>
  <style>
    :root {{ color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; background: #0b1220; color: #e5edf9; }}
    * {{ box-sizing: border-box; }} body {{ margin: 0; padding: 32px; }}
    main {{ max-width: 1440px; margin: auto; }}
    header {{ margin-bottom: 28px; }} h1 {{ margin: 0 0 8px; font-size: clamp(1.6rem, 3vw, 2.5rem); }}
    header p, .caption, .metric-detail {{ color: #91a1bc; }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 14px; margin: 24px 0; }}
    .metric, .panel {{ background: #121d30; border: 1px solid #24324a; border-radius: 16px; padding: 20px; }}
    .metric-label {{ margin: 0; color: #9fb0ca; font-size: .83rem; text-transform: uppercase; letter-spacing: .06em; }}
    .metric-value {{ margin: 12px 0 6px; color: #79d5c2; font-size: clamp(1.4rem, 2vw, 2rem); font-weight: 750; overflow-wrap: anywhere; }}
    .metric-detail, .metric-delta {{ margin: 4px 0 0; font-size: .82rem; }} .metric-delta {{ color: #8adab9; }}
    .charts {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 480px), 1fr)); gap: 16px; }}
    .panel h2 {{ margin-top: 0; }} .caption {{ margin: 0 0 8px; }} li {{ margin: 10px 0; line-height: 1.5; }}
    .empty {{ padding: 20px; color: #91a1bc; }} footer {{ margin-top: 24px; color: #71819d; font-size: .8rem; }}
    @media (max-width: 640px) {{ body {{ padding: 16px; }} }}
  </style>
</head>
<body><main>
  <header><h1>Interactive EDA Dashboard</h1><p>{title} · Explore charts with hover, zoom, pan, and legend controls.</p></header>
  <section class="metrics" aria-label="Key performance indicators">{cards_html}</section>
  <section class="charts" aria-label="Interactive charts">{charts_html}</section>
  {insight_section}
  <footer>Generated from the dataset with validated metrics and interactive Plotly charts.</footer>
</main></body></html>"""
