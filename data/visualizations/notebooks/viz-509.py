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
    mo.md(
        """
        # Communicable Disease Deaths — Methodology

        Documents the data pipeline behind viz-509.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DTH-COMM-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_keywords = ['World', 'Africa', 'Asia', 'Europe', 'OECD', 'income', 'dividend', 'Arab', 'Euro',
                    'Caribbean', 'Pacific', 'Latin', 'Sub-Saharan', 'East Asia', 'Middle East',
                    'North America', 'Fragile', 'IDA', 'IBRD', 'Heavily', 'Least', 'Small',
                    'states', 'development', 'South Asia', 'Pre-', 'Late-', 'Early-', 'demographic']
    v2000 = {}
    v2019 = {}
    for r in data:
        c = r['countryName']
        if any(kw.lower() in c.lower() for kw in agg_keywords):
            continue
        if r['value'] is None:
            continue
        if r['year'] == 2000:
            v2000[c] = r['value']
        elif r['year'] == 2019:
            v2019[c] = r['value']
    common = set(v2000) & set(v2019)
    print(f"Countries with both 2000 and 2019 data: {len(common)}")
    return agg_keywords, common, v2000, v2019


@app.cell
def _(common, v2000, v2019):
    pairs = [(c, round(v2000[c], 1), round(v2019[c], 1)) for c in common]
    pairs.sort(key=lambda x: -x[1])
    high = [p for p in pairs if p[1] > 35]
    print(f"High-burden countries (>35% in 2000): {len(high)}")
    return high, pairs


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — compare two points in time across many entities
        - **Country selection**: Countries with highest communicable disease burden in 2000, plus a few
          low-burden countries (European) for visual contrast
        - **Time points**: 2000 (first available) and 2019 (last pre-COVID full year)
        - **Color**: Magnitude of improvement — greens for large drops, amber/red for small drops or rises
        - **Story**: Dramatic epidemiological transition in many African countries; HIV treatment rollout visible
        """
    )
    return


@app.cell
def _(json, high, v2000, v2019):
    selected_high = [p[0] for p in high[:13]]
    selected_low = ['India', 'Indonesia', 'Haiti', 'Hungary', 'Croatia', 'Italy', 'Denmark', 'Japan']
    all_selected = selected_high + [c for c in selected_low if c in v2000 and c in v2019]
    chart_data = [
        {"n": c, "a": round(v2000[c], 1), "b": round(v2019[c], 1)}
        for c in all_selected
        if c in v2000 and c in v2019
    ]
    chart_data.sort(key=lambda x: -x['a'])
    print(json.dumps(chart_data, separators=(",", ":")))
    return all_selected, chart_data, selected_high, selected_low


if __name__ == "__main__":
    app.run()
