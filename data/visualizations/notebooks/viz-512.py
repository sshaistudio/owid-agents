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
        # GDP per Capita PPP (constant 2021 $) -- Methodology

        Documents the data pipeline behind viz-512.
        Dataset: wb--NY-GDP-PCAP-PP-KD (World Bank NY.GDP.PCAP.PP.KD)
        Metric: GDP per capita adjusted for purchasing power parity, constant 2021 international $.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GDP-PCAP-PP-KD.json"
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
        'countries', 'states', 'economies', 'SAR', 'North America',
    ]

    def is_country(name):
        return not any(w.lower() in name.lower() for w in skip_words)

    individual = [p for p in data if p["value"] is not None and is_country(p["countryName"])]
    print(f"Individual country data points: {len(individual)}")
    return individual, is_country, skip_words


@app.cell
def _(individual, json):
    countries = {}
    for p in individual:
        c = p["country"]
        if c not in countries:
            countries[c] = {"name": p["countryName"], "pts": []}
        countries[c]["pts"].append({"y": p["year"], "v": p["value"]})

    select = ['CN', 'IN', 'ID', 'KR', 'BR', 'DE', 'JP']
    years = list(range(1990, 2025))
    chart_data = []
    for c in select:
        if c in countries:
            pts = {p["y"]: p["v"] for p in countries[c]["pts"]}
            series = [round(pts[y]) if y in pts else None for y in years]
            non_null = sum(1 for v in series if v is not None)
            if non_null >= 20:
                chart_data.append({"n": countries[c]["name"], "s": series, "y0": 1990, "step": 1})

    for s in chart_data:
        vals = [v for v in s["s"] if v is not None]
        print(f"  {s['n']}: ${vals[0]:,} -> ${vals[-1]:,}")
    print()
    print(json.dumps(chart_data, separators=(",", ":")))
    return c, chart_data, countries, non_null, pts, s, select, series, vals, years


if __name__ == "__main__":
    app.run()
