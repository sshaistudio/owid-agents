import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import json
    from pathlib import Path
    return json, mo, Path


@app.cell
def _(mo):
    mo.md("""
    # Diabetes Prevalence — Methodology

    Horizontal bar chart showing the top 25 countries by diabetes prevalence
    among adults aged 20–79 as of 2024.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-STA-DIAB-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    pts = [p for p in data if p["value"] is not None and p["year"] == 2024]
    skip = ["World","income","Asia","Africa","Europe","America","Arab","Caribbean","Pacific","IDA","IBRD","OECD","Euro","dividend","fragile","indebted","Island"]
    pts = [p for p in pts if not any(w.lower() in p["countryName"].lower() for w in skip)]
    pts.sort(key=lambda x: x["value"], reverse=True)
    top25 = pts[:25]
    print(f"Top 25 countries by diabetes prevalence in 2024:")
    for p in top25:
        print(f"  {p['countryName']}: {p['value']:.1f}%")
    return pts, top25


@app.cell
def _(mo):
    mo.md("""
    ## Design Rationale

    - **Chart type**: Horizontal bar chart — best for ranked single-metric comparisons
    - **Country selection**: Top 25 by prevalence in 2024
    - **Year**: 2024 (most recent with near-global coverage)
    - **Highlights**: Kiribati (24.6%) and French Polynesia (22.8%) lead globally;
      Middle East and Pacific Islands cluster at the top; Sub-Saharan Africa sees
      much lower rates, partly due to age structure
    """)
    return


@app.cell
def _(json, top25):
    chart_data = [{"n": p["countryName"], "v": round(p["value"], 1)} for p in top25]
    print(json.dumps(chart_data))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
