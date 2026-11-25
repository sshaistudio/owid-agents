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
    # Lifetime Risk of Maternal Death — Methodology

    Slope chart comparing the lifetime risk of maternal death (%) between 1990
    and 2023 for the 20 highest-risk countries in 1990.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-MMR-RISK-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    pts_1990 = {p["countryName"]: round(p["value"], 4) for p in data if p["year"] == 1990 and p["value"] is not None}
    pts_2023 = {p["countryName"]: round(p["value"], 4) for p in data if p["year"] == 2023 and p["value"] is not None}
    skip = ["World","income","Asia","Africa","Europe","America","Arab","Caribbean","Pacific","IDA","IBRD","OECD","Euro","dividend","fragile","indebted","Island","Eastern","Western","Central","Northern","Southern","Saharan","demographic","Pre-","Low-","Middle","High-","Least","conflict","Violence","classification","situations","South","East","Sub"]
    common = {c for c in set(pts_1990.keys()) & set(pts_2023.keys()) if not any(w.lower() in c.lower() for w in skip)}
    slope = [(c, pts_1990[c], pts_2023[c]) for c in common]
    slope.sort(key=lambda x: x[1], reverse=True)
    selected = slope[:20]
    print(f"Top 20 countries by 1990 maternal mortality risk:")
    for c, a, b in selected:
        r = (a - b) / a * 100
        print(f"  {c}: {a:.2f}% -> {b:.2f}%  ({r:.0f}% reduction)")
    return pts_1990, pts_2023, selected, slope


@app.cell
def _(mo):
    mo.md("""
    ## Design Rationale

    - **Chart type**: Slope chart — before/after comparison reveals disparate progress
    - **Country selection**: 20 countries with highest 1990 risk
    - **Time range**: 1990 vs 2023 (full available range)
    - **Highlights**: Bangladesh reduced risk by 94%, Bhutan by 98% — extraordinary
      progress; Chad and Congo reduced by less than 50% and remain dangerously high;
      color encodes percentage reduction
    """)
    return


@app.cell
def _(json, selected):
    chart_data = [{"n": c, "a": a, "b": b} for c, a, b in selected]
    print(json.dumps(chart_data))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
