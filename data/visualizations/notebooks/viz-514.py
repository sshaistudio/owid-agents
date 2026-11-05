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
        # Current Account Balance (% of GDP) -- Methodology

        Documents the data pipeline behind viz-514.
        Dataset: wb--BN-CAB-XOKA-GD-ZS (World Bank BN.CAB.XOKA.GD.ZS)
        Metric: Current account balance as % of GDP. Positive = surplus, negative = deficit.
        Comparison: 2000 vs 2022 for major economies.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--BN-CAB-XOKA-GD-ZS.json"
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
        'countries', 'states', 'economies', 'dividend',
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

    key_c = ["DE", "NL", "NO", "JP", "CN", "KR", "AU", "CA", "FR", "IT", "IN", "BR"]
    slope = []
    for c in key_c:
        if c in countries:
            pts = {p["y"]: p["v"] for p in countries[c]["pts"]}
            a = pts.get(2000)
            b = pts.get(2022) or pts.get(2021)
            if a is not None and b is not None:
                slope.append({"n": countries[c]["name"], "a": round(a, 1), "b": round(b, 1)})

    for s in slope:
        print(f"  {s['n']}: {s['a']:+.1f}% -> {s['b']:+.1f}%")
    print()
    print(json.dumps(slope, separators=(",", ":")))
    return a, b, c, countries, key_c, pts, s, slope


if __name__ == "__main__":
    app.run()
