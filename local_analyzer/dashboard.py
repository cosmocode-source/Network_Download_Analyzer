import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from data_fetcher import load_data
from analytics import server_summary, compute_best_server, compute_percentage_difference
from datetime import datetime
import pandas as pd
from report_logic import interpret_latency, interpret_handshake, interpret_throughput, interpret_variance

# ── Brand & colour system ────────────────────────────────────────────────────
BRAND       = "#1A56DB"
BRAND_LIGHT = "#EBF2FF"
BRAND_DARK  = "#1040B0"
SUCCESS     = "#0E9F6E"
WARNING     = "#C27803"
DANGER      = "#E02424"

BG          = "#F3F4F6"
SURFACE     = "#FFFFFF"
BORDER      = "#E5E7EB"
BORDER_MED  = "#D1D5DB"

TEXT_H      = "#111827"
TEXT_BODY   = "#374151"
TEXT_MUTED  = "#6B7280"

SERIES = [BRAND, SUCCESS, WARNING, DANGER, "#7C3AED", "#DB6B1A", "#0E9F9F"]

# ── Plotly template ──────────────────────────────────────────────────────────
BASE_LAYOUT = dict(
    template="plotly_white",
    paper_bgcolor=SURFACE,
    plot_bgcolor="#FAFAFA",
    font=dict(family="'IBM Plex Sans', 'Segoe UI', sans-serif", color=TEXT_BODY, size=12),
    title_font=dict(family="'DM Sans', 'Segoe UI', sans-serif", color=TEXT_H, size=14),
    legend=dict(bgcolor=SURFACE, bordercolor=BORDER, borderwidth=1, font=dict(size=11, color=TEXT_BODY)),
    xaxis=dict(gridcolor=BORDER, linecolor=BORDER_MED, tickfont=dict(color=TEXT_MUTED, size=11)),
    yaxis=dict(gridcolor=BORDER, linecolor=BORDER_MED, tickfont=dict(color=TEXT_MUTED, size=11)),
    margin=dict(l=52, r=24, t=56, b=44),
    hoverlabel=dict(bgcolor=SURFACE, bordercolor=BORDER, font_color=TEXT_BODY,
                    font_family="'IBM Plex Sans', sans-serif"),
)

def styled(fig, **kw):
    fig.update_layout(**{**BASE_LAYOUT, **kw})
    return fig

# ── CSS ──────────────────────────────────────────────────────────────────────
STYLES = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
    background: #F3F4F6;
    color: #374151;
    font-family: 'IBM Plex Sans', 'Segoe UI', sans-serif;
    font-size: 14px;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
}

/* ── Topbar ── */
.topbar {
    background: #FFFFFF;
    border-bottom: 1px solid #E5E7EB;
    padding: 0 40px;
    height: 62px;
    display: flex;
    align-items: center;
    gap: 14px;
    position: sticky;
    top: 0;
    z-index: 50;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.topbar-logo {
    width: 30px; height: 30px;
    background: #1A56DB;
    border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    font-size: 15px;
}
.topbar-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #111827;
    letter-spacing: -0.01em;
}
.topbar-divider { width: 1px; height: 18px; background: #E5E7EB; }
.topbar-sub { font-size: 12px; color: #9CA3AF; font-weight: 400; }
.topbar-right { margin-left: auto; display: flex; align-items: center; gap: 18px; }

.timestamp {
    font-size: 12px;
    color: #9CA3AF;
    display: flex;
    align-items: center;
    gap: 6px;
}
.timestamp-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #0E9F6E;
    flex-shrink: 0;
}

.export-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #1A56DB;
    color: white;
    border: none;
    padding: 7px 16px;
    border-radius: 6px;
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.15s, box-shadow 0.15s;
    box-shadow: 0 1px 3px rgba(26,86,219,0.25);
    letter-spacing: 0.01em;
}
.export-btn:hover { background: #1040B0; box-shadow: 0 3px 10px rgba(26,86,219,0.3); }

/* ── Page ── */
.page { max-width: 1380px; margin: 0 auto; padding: 36px 40px 80px; }

.page-header { margin-bottom: 32px; }
.page-header h1 {
    font-family: 'DM Sans', sans-serif;
    font-size: 21px; font-weight: 700;
    color: #111827; letter-spacing: -0.02em; margin-bottom: 5px;
}
.page-header p { font-size: 13px; color: #9CA3AF; }

/* ── Section Labels ── */
.section-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 10.5px; font-weight: 600;
    letter-spacing: 0.09em; text-transform: uppercase;
    color: #9CA3AF;
    margin: 40px 0 16px;
    display: flex; align-items: center; gap: 12px;
}
.section-label::after { content: ''; flex: 1; height: 1px; background: #E5E7EB; }

/* ── KPI cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 20px 22px 18px;
    display: flex; flex-direction: column; gap: 10px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    transition: box-shadow 0.15s, transform 0.15s;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.kpi-card.kpi-blue::before  { background: #1A56DB; }
.kpi-card.kpi-green::before { background: #0E9F6E; }
.kpi-card.kpi-amber::before { background: #C27803; }
.kpi-card:hover { box-shadow: 0 4px 14px rgba(0,0,0,0.08); transform: translateY(-1px); }
.kpi-card-top { display: flex; align-items: center; justify-content: space-between; }
.kpi-badge {
    font-size: 10px; font-weight: 600;
    letter-spacing: 0.05em; text-transform: uppercase;
    padding: 3px 8px; border-radius: 4px;
}
.kpi-badge.blue  { background: #EBF2FF; color: #1A56DB; }
.kpi-badge.green { background: #ECFDF5; color: #0E9F6E; }
.kpi-badge.amber { background: #FFFBEB; color: #C27803; }
.kpi-label { font-size: 12px; color: #6B7280; font-weight: 400; }
.kpi-value {
    font-family: 'DM Sans', sans-serif;
    font-size: 20px; font-weight: 700;
    color: #111827; letter-spacing: -0.02em; line-height: 1.2;
}
.kpi-meta { font-size: 11px; color: #9CA3AF; }

/* ── Interpretation cards ── */
.interp-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 8px; }
.interp-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 18px 20px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.interp-card-label {
    font-size: 10.5px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.07em;
    color: #9CA3AF; margin-bottom: 7px;
    display: flex; align-items: center; gap: 6px;
}
.interp-card-text { font-size: 13px; color: #374151; line-height: 1.55; }

/* ── Graph cards ── */
.graph-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.graph-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.graph-card.full { grid-column: 1 / -1; }

/* ── Tables ── */
.table-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.table-wrapper { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
thead tr { background: #F9FAFB; border-bottom: 2px solid #E5E7EB; }
thead th {
    padding: 11px 16px; text-align: left;
    font-family: 'DM Sans', sans-serif;
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.05em; text-transform: uppercase; color: #6B7280;
    white-space: nowrap;
}
thead th:not(:first-child) { text-align: right; }

tbody tr { border-bottom: 1px solid #F3F4F6; transition: background 0.1s; }
tbody tr:last-child { border-bottom: none; }
tbody tr:hover { background: #F9FAFB; }
tbody td { padding: 10px 16px; color: #374151; vertical-align: middle; }
tbody td.num { text-align: right; font-variant-numeric: tabular-nums; }

/* Hourly table specifics */
.hour-cell {
    font-family: 'DM Sans', sans-serif;
    font-size: 12px; font-weight: 600;
    color: #111827;
    background: #F9FAFB;
    white-space: nowrap;
    border-right: 2px solid #E5E7EB;
    vertical-align: middle !important;
}
.hour-group-first td { border-top: 2px solid #E5E7EB; }
.hour-group-last td  { border-bottom: 2px solid #E5E7EB !important; }
.server-cell { font-weight: 500; color: #1A56DB; }

/* Summary table first col */
.summary-table tbody td:first-child { font-weight: 600; color: #111827; text-align: left; }
"""

# ── Data ─────────────────────────────────────────────────────────────────────
df = load_data()
LAST_UPDATED = datetime.now().strftime("%d %b %Y, %H:%M")

app = dash.Dash(__name__)
server = app.server

app.index_string = f"""<!DOCTYPE html>
<html>
  <head>
    {{%metas%}}
    <title>NetPulse — Network Performance Analyzer</title>
    {{%favicon%}}
    {{%css%}}
    <style>{STYLES}</style>
  </head>
  <body>
    {{%app_entry%}}
    <footer>
      {{%config%}}
      {{%scripts%}}
      {{%renderer%}}
    </footer>
  </body>
</html>"""

# ── Shared topbar ─────────────────────────────────────────────────────────────
def topbar(show_export=True):
    right_items = [
        html.Div([
            html.Div(className="timestamp-dot"),
            html.Span(f"Last updated: {LAST_UPDATED}"),
        ], className="timestamp"),
    ]
    if show_export:
        right_items += [
            dcc.Download(id="csv-download"),
            html.Button("↓  Export CSV", id="export-btn",
                        className="export-btn", n_clicks=0),
        ]
    return html.Div([
        html.Div("📡", className="topbar-logo"),
        html.Span("NetPulse", className="topbar-title"),
        html.Div(className="topbar-divider"),
        html.Span("TCP Network Performance Analyzer", className="topbar-sub"),
        html.Div(right_items, className="topbar-right"),
    ], className="topbar")


# ── Empty state ───────────────────────────────────────────────────────────────
if df.empty:
    app.layout = html.Div([
        topbar(show_export=False),
        html.Div([
            html.Div([
                html.H1("No Data Available"),
                html.P("No records found in MongoDB Atlas. Check your connection and try again."),
            ], className="page-header"),
        ], className="page"),
    ])

# ── Full dashboard ────────────────────────────────────────────────────────────
else:
    summary = server_summary(df)
    summary = compute_percentage_difference(summary)
    best    = compute_best_server(summary)
    s       = summary.reset_index()

    # Hourly data
    hourly_df = df.copy()
    hourly_df["hour"] = hourly_df["timestamp"].dt.floor("h")

    hourly_metrics = (
        hourly_df.groupby("hour")
        .agg(
            avg_throughput=("throughput_Mbps", "mean"),
            avg_latency=("latency_ms", "mean"),
            measurements=("server_name", "count")
        )
        .reset_index()
    )

    server_hour_usage = (
        hourly_df.groupby(["hour", "server_name"])
        .size()
        .reset_index(name="tests")
    )

    # Hourly table: one row per (hour, server), aggregated — so each timestamp shows all servers
    hourly_table = (
        hourly_df
        .groupby(["hour", "server_name"], sort=True)
        .agg(
            throughput_Mbps=("throughput_Mbps", "mean"),
            latency_ms=("latency_ms", "mean"),
            tcp_handshake_ms=("tcp_handshake_ms", "mean"),
        )
        .reset_index()
        .sort_values(["hour", "server_name"])
    )

    # Build grouped rows with rowspan for the hour column
    def build_hourly_rows(ht):
        rows = []
        grouped = ht.groupby("hour", sort=True)
        for hour, group in grouped:
            group = group.reset_index(drop=True)
            count = len(group)
            hour_label = pd.Timestamp(hour).strftime("%d %b %Y %H:%M")
            for j, row in group.iterrows():
                row_cells = []
                if j == 0:
                    row_cells.append(
                        html.Td(hour_label, rowSpan=count, className="hour-cell")
                    )
                row_cells += [
                            html.Td(row["server_name"], className="server-cell"),
                            html.Td(f"{row['throughput_Mbps']:.2f}",   className="num"),
                            html.Td(f"{row['latency_ms']:.2f}",         className="num"),
                            html.Td(f"{row['tcp_handshake_ms']:.2f}",   className="num"),
                            ]
                classes = []
                if j == 0:
                    classes.append("hour-group-first")
                if j == count - 1:
                    classes.append("hour-group-last")
                rows.append(html.Tr(row_cells, className=" ".join(classes) if classes else None))
        return rows

    best_latency_value   = summary.loc[best["best_latency"],   "avg_latency"]
    best_throughput_value = summary.loc[best["best_throughput"],"avg_throughput"]
    best_variance_value  = summary.loc[best["most_stable"],    "stability"]

    latency_text    = interpret_latency(best_latency_value)
    throughput_text = interpret_throughput(best_throughput_value)
    variance_text   = interpret_variance(best_variance_value)

    def line_fig(x, y, title):
        fig = px.line(df, x=x, y=y, color="server_name",
                      color_discrete_sequence=SERIES, title=title)
        fig.update_traces(line_width=2.5)
        return styled(fig)

    def bar_fig(x, y, title):
        fig = go.Figure(go.Bar(
            x=s[x], y=s[y],
            marker=dict(color=SERIES[:len(s)], opacity=0.9, line=dict(width=0)),
        ))
        return styled(fig, title_text=title)

    latency_fig    = line_fig("timestamp", "latency_ms",      "Latency Over Time (ms)")
    throughput_fig = line_fig("timestamp", "throughput_Mbps", "Throughput Over Time (Mbps)")
    handshake_fig  = bar_fig("server_name", "avg_handshake",  "Avg TCP Handshake Time (ms)")
    tput_cmp_fig   = bar_fig("server_name", "avg_throughput", "Avg Throughput (Mbps)")
    stability_fig  = bar_fig("server_name", "stability",      "Transfer Stability")
    instance_fig   = bar_fig("server_name", "instances",      "Measurement Instances per Server")

    traffic_fig = px.line(
        hourly_metrics, x="hour", y="avg_throughput",
        title="Hourly Network Throughput Trend"
    )
    traffic_fig.update_traces(line_width=2.5)
    traffic_fig = styled(traffic_fig)

    server_usage_fig = px.bar(
        server_hour_usage, x="hour", y="tests", color="server_name",
        title="Server Usage Per Hour",
        color_discrete_sequence=SERIES
    )
    server_usage_fig = styled(server_usage_fig)

    app.layout = html.Div([
        topbar(show_export=True),
        html.Div([

            # ── Page header ──────────────────────────────────────────────────
            html.Div([
                html.H1("Network Performance Overview"),
                html.P("Real-time TCP metrics and server benchmarking across all monitored endpoints."),
            ], className="page-header"),

            # ── KPI cards ────────────────────────────────────────────────────
            html.Div("Best performing servers", className="section-label"),
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("Latency", className="kpi-label"),
                        html.Span("Lowest", className="kpi-badge blue"),
                    ], className="kpi-card-top"),
                    html.Div(best["best_latency"], className="kpi-value"),
                    html.Div("Best measured avg latency", className="kpi-meta"),
                ], className="kpi-card kpi-blue"),

                html.Div([
                    html.Div([
                        html.Span("Throughput", className="kpi-label"),
                        html.Span("Highest", className="kpi-badge green"),
                    ], className="kpi-card-top"),
                    html.Div(best["best_throughput"], className="kpi-value"),
                    html.Div("Best measured avg throughput", className="kpi-meta"),
                ], className="kpi-card kpi-green"),

                html.Div([
                    html.Div([
                        html.Span("Stability", className="kpi-label"),
                        html.Span("Most Stable", className="kpi-badge amber"),
                    ], className="kpi-card-top"),
                    html.Div(best["most_stable"], className="kpi-value"),
                    html.Div("Lowest transfer variance", className="kpi-meta"),
                ], className="kpi-card kpi-amber"),
            ], className="kpi-grid"),

            # ── Network interpretation ───────────────────────────────────────
            html.Div("Network interpretation", className="section-label"),
            html.Div([
                html.Div([
                    html.Div(["📶  ", "Latency"], className="interp-card-label"),
                    html.Div(latency_text, className="interp-card-text"),
                ], className="interp-card"),
                html.Div([
                    html.Div(["⚡  ", "Throughput"], className="interp-card-label"),
                    html.Div(throughput_text, className="interp-card-text"),
                ], className="interp-card"),
                html.Div([
                    html.Div(["📊  ", "Stability"], className="interp-card-label"),
                    html.Div(variance_text, className="interp-card-text"),
                ], className="interp-card"),
            ], className="interp-grid"),

            # ── Time-series ──────────────────────────────────────────────────
            html.Div("Time-series trends", className="section-label"),
            dcc.Loading(type="circle", color=BRAND, children=html.Div([
                html.Div(dcc.Graph(figure=latency_fig,    config={"displayModeBar": False}), className="graph-card full"),
                html.Div(dcc.Graph(figure=throughput_fig, config={"displayModeBar": False}), className="graph-card full"),
                html.Div(dcc.Graph(figure=traffic_fig,    config={"displayModeBar": False}), className="graph-card full"),
            ], className="graph-grid-2")),

            # ── Server comparison ────────────────────────────────────────────
            html.Div("Server comparison", className="section-label"),
            dcc.Loading(type="circle", color=BRAND, children=html.Div([
                html.Div(dcc.Graph(figure=handshake_fig,    config={"displayModeBar": False}), className="graph-card"),
                html.Div(dcc.Graph(figure=tput_cmp_fig,     config={"displayModeBar": False}), className="graph-card"),
                html.Div(dcc.Graph(figure=stability_fig,    config={"displayModeBar": False}), className="graph-card"),
                html.Div(dcc.Graph(figure=instance_fig,     config={"displayModeBar": False}), className="graph-card"),
                html.Div(dcc.Graph(figure=server_usage_fig, config={"displayModeBar": False}), className="graph-card full"),
            ], className="graph-grid-2")),

            # ── Hourly server table ──────────────────────────────────────────
            html.Div("Server activity by hour", className="section-label"),
            html.Div(
                html.Div(
                    html.Table([
                        html.Thead(html.Tr([
                            html.Th("Hour"),
                            html.Th("Server"),
                            html.Th("Throughput (Mbps)"),
                            html.Th("Latency (ms)"),
                            html.Th("Handshake (ms)"),
                        ])),
                        html.Tbody(build_hourly_rows(hourly_table)),
                    ]),
                    className="table-wrapper"
                ),
                className="table-card",
                style={"marginBottom": "14px"},
            ),

            # ── Summary table ────────────────────────────────────────────────
            html.Div("Summary table", className="section-label"),
            html.Div(
                html.Div(
                    html.Table([
                        html.Thead(html.Tr([html.Th(col) for col in s.columns])),
                        html.Tbody([
                            html.Tr([html.Td(s.iloc[i][col]) for col in s.columns])
                            for i in range(len(s))
                        ]),
                    ], className="summary-table"),
                    className="table-wrapper"
                ),
                className="table-card",
            ),

        ], className="page"),
    ])

    @app.callback(
        Output("csv-download", "data"),
        Input("export-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def export_csv(n):
        return dcc.send_data_frame(df.to_csv, "network_performance_export.csv", index=False)

if __name__ == "__main__":
    app.run(debug=True)