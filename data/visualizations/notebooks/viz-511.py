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
    # Primary School Net Enrollment Rate — Methodology

    Slope chart comparing the adjusted net enrollment rate for primary school
    between 2000 and 2017 for 20 countries with the most dramatic changes.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRM-TENR.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    pts = [p for p in data if p["value"] is not None]
    pts_2000 = {p["countryName"]: round(p["value"], 1) for p in pts if p["year"] == 2000}
    pts_2017 = {p["countryName"]: round(p["value"], 1) for p in pts if p["year"] == 2017}
    skip = ["World","income","Asia","Africa","Europe","America","Arab","Caribbean","Pacific","IDA","IBRD","OECD","Euro","dividend","fragile","indebted","Island","Eastern","Western","Central","Northern","Southern","Saharan"]
    common = {c for c in set(pts_2000.keys()) & set(pts_2017.keys()) if not any(w.lower() in c.lower() for w in skip)}
    slope = [(c, pts_2000[c], pts_2017[c], pts_2017[c] - pts_2000[c]) for c in common]
    slope.sort(key=lambda x: x[3], reverse=True)
    selected = slope[:12] + slope[-8:]
    print(f"Selected {len(selected)} countries: top 12 improvers + 8 decliners")
    for c, a, b, diff in selected:
        print(f"  {c}: {a} -> {b} ({diff:+.1f})")
    return pts_2000, pts_2017, selected, slope


@app.cell
def _(mo):
    mo.md("""
    ## Design Rationale

    - **Chart type**: Slope chart — ideal for before/after comparisons across many countries
    - **Country selection**: Top 12 improvers and 8 biggest decliners (by absolute pp change)
    - **Time range**: 2000 vs 2017 — most recent year with 100+ country coverage
    - **Highlights**: Sub-Saharan Africa saw dramatic gains (Burundi +54 pp, Burkina Faso +40 pp);
      some middle-income countries saw modest declines
    """)
    return


@app.cell
def _(json, selected):
    chart_data = [{"n": c, "a": a, "b": b} for c, a, b, diff in selected]
    print(json.dumps(chart_data))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
