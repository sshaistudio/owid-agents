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
        # Lifetime Risk of Maternal Death -- Methodology

        Documents the data pipeline behind viz-513.
        Dataset: wb--SH-MMR-RISK-ZS (World Bank SH.MMR.RISK.ZS)
        Metric: Probability (%) that a 15-year-old girl will eventually die from a maternal cause,
        given fertility and mortality rates in the given year.
        """
    )
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
    skip_words = [
        'World', 'Africa', 'Asia', 'Europe', 'Middle', 'Caribbean', 'Pacific',
        'Central', 'Eastern', 'Western', 'Northern', 'Southern', 'Sub-Saharan',
        'Latin', 'Arab', 'OECD', 'low income', 'middle income', 'high income',
        'fragile', 'Heavily', 'IDA', 'IBRD', 'Euro', 'small states', 'island',
        'countries', 'states', 'economies', 'dividend', 'FCV', 'Conflict',
        'situations', 'demographic',
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

    slope_data = []
    for c, info in countries.items():
        pts = {p["y"]: p["v"] for p in info["pts"]}
        a = pts.get(1990) or pts.get(1991)
        b = pts.get(2022) or pts.get(2021)
        if a and b and a >= 2.0:
            slope_data.append({"n": info["name"], "a": round(a, 3), "b": round(b, 3)})

    slope_data.sort(key=lambda x: x["a"], reverse=True)
    print(f"High-burden countries (>=2% in 1990): {len(slope_data)}")
    for s in slope_data:
        chg = (s["b"] - s["a"]) / s["a"] * 100
        print(f"  {s['n']}: {s['a']:.2f}% -> {s['b']:.2f}% ({chg:+.0f}%)")
    print()
    print(json.dumps(slope_data[:15], separators=(",", ":")))
    return c, countries, info, pts, s, slope_data


if __name__ == "__main__":
    app.run()
