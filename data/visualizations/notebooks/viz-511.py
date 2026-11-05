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
        # Premature NCD Mortality Risk, Ages 30-70 -- Methodology

        Documents the data pipeline behind viz-511.
        Dataset: wb--SH-DYN-NCOM-ZS (World Bank SH.DYN.NCOM.ZS)
        Metric: Probability (%) of dying between ages 30 and 70 from CVD, cancer, diabetes, or CRD.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DYN-NCOM-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    skip_words = [
        'World', 'Africa', 'Asia', 'Europe', 'Middle', 'Caribbean', 'Pacific',
        'Central', 'Eastern', 'Western', 'Northern', 'Southern', 'Sub-Saharan',
        'Latin', 'Arab', 'OECD', 'low income', 'middle income', 'high income',
        'fragile', 'Heavily', 'IDA', 'IBRD', 'Euro', 'small states', 'island',
        'countries', 'states', 'economies',
    ]

    def is_country(name):
        return not any(w.lower() in name.lower() for w in skip_words)

    individual = [p for p in data if p["value"] is not None and is_country(p["countryName"])]
    print(f"Individual country data points: {len(individual)}")
    return individual, is_country, skip_words


@app.cell
def _(individual):
    countries = {}
    for p in individual:
        c = p["country"]
        if c not in countries:
            countries[c] = {"name": p["countryName"], "pts": []}
        countries[c]["pts"].append({"y": p["year"], "v": p["value"]})

    c2021 = {c: next((x["v"] for x in info["pts"] if x["y"] == 2021), None)
             for c, info in countries.items()}
    c2021 = {c: v for c, v in c2021.items() if v is not None}
    sorted_c = sorted(c2021.items(), key=lambda x: x[1], reverse=True)
    print(f"Countries: {len(countries)}, with 2021 data: {len(c2021)}")
    print(f"Range: {min(c2021.values()):.1f}% - {max(c2021.values()):.1f}%")
    return c2021, countries, sorted_c


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows how 11 countries' premature NCD mortality evolved 2000-2021
        - **Country selection**: Mix of high-burden (Fiji, Afghanistan), medium (India, Indonesia, China),
          and low-burden (Korea, Japan, Australia, Germany) to show divergence and convergence
        - **Color**: Improvement-band coloring by percent decline -- big decliners green, stagnant/rising orange
        - **Highlights**: Korea halved its rate (16.9% to 6.9%); India barely changed; Fiji still near 40%
        """
    )
    return


@app.cell
def _(countries, json):
    select = ['FJ', 'AF', 'BG', 'IN', 'ID', 'CN', 'BR', 'DE', 'JP', 'KR', 'AU']
    years = list(range(2000, 2022))
    chart_data = []
    for c in select:
        if c in countries:
            pts = {p["y"]: p["v"] for p in countries[c]["pts"]}
            series = [round(pts[y], 1) if y in pts else None for y in years]
            non_null = sum(1 for v in series if v is not None)
            if non_null >= 15:
                chart_data.append({"n": countries[c]["name"], "s": series, "y0": 2000, "step": 1})
    print(f"Chart series: {len(chart_data)}")
    for s in chart_data:
        vals = [v for v in s["s"] if v is not None]
        v0, v1 = vals[0], vals[-1]
        chg = (v1 - v0) / v0 * 100
        print(f"  {s['n']}: {v0} -> {v1} ({chg:+.0f}%)")
    print()
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, c, non_null, pts, s, select, series, vals, years


if __name__ == "__main__":
    app.run()
