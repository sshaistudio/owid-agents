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
        # Hepatitis B Vaccination Coverage (HepB3) -- Methodology

        Documents the data pipeline behind viz-515.
        Dataset: wb--SH-IMM-HEPB (World Bank SH.IMM.HEPB)
        Metric: HepB3 immunization coverage among 1-year-old children (%).
        3-dose hepatitis B vaccine series, which confers ~95% protection.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-IMM-HEPB.json"
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
        'countries', 'states', 'economies', 'dividend', 'FCV', 'Conflict',
        'situations', 'Fragility',
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

    # Countries with notable journeys
    select = ['FR', 'AT', 'BB', 'CI', 'BJ', 'CN', 'GE', 'IN', 'BD', 'KE', 'ET', 'GH']
    already_high = ['IR', 'KZ', 'CU', 'FJ']

    years = list(range(2000, 2025))
    chart_data = []
    for c in select + already_high:
        if c in countries:
            pts = {p["y"]: p["v"] for p in countries[c]["pts"]}
            series = [round(pts[y]) if y in pts else None for y in years]
            non_null = sum(1 for v in series if v is not None)
            if non_null >= 10:
                chart_data.append({"n": countries[c]["name"], "s": series, "y0": 2000, "step": 1})

    for s in chart_data:
        vals = [v for v in s["s"] if v is not None]
        v0 = vals[0]
        vl = vals[-1]
        print(f"  {s['n']}: {v0}% -> {vl}%")
    print()
    print(json.dumps(chart_data, separators=(",", ":")))
    return c, chart_data, countries, non_null, pts, s, select, series, vals, years


if __name__ == "__main__":
    app.run()
