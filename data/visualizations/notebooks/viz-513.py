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
    # Labor Force Participation Rate — Methodology

    Trend lines for 8 major economies showing labor force participation
    (% of population 15–64) from 1990 to 2024.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-TLF-ACTI-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    sel_countries = ["Brazil", "China", "France", "Germany", "India", "Italy", "Japan", "Korea, Rep."]
    pts = [p for p in data if p["value"] is not None and p["countryName"] in sel_countries]
    country_data = {}
    for p in pts:
        c = p["countryName"]
        if c not in country_data:
            country_data[c] = []
        country_data[c].append({"y": p["year"], "v": round(p["value"], 1)})
    for c in country_data:
        country_data[c].sort(key=lambda x: x["y"])
        first = country_data[c][0]
        last = country_data[c][-1]
        print(f"{c}: {first['v']}% ({first['y']}) -> {last['v']}% ({last['y']})")
    return country_data, pts, sel_countries


@app.cell
def _(mo):
    mo.md("""
    ## Design Rationale

    - **Chart type**: Trend lines — multi-entity time series comparison
    - **Country selection**: 8 major economies representing different trajectories
    - **Time range**: 1990–2024 (full available range)
    - **Highlights**: Japan rose 12 pp since 1990 driven by Abenomics reforms and
      female workforce inclusion; China declined 10 pp as economy shifted from
      labor-intensive agriculture; Germany climbed steadily post-reunification
    """)
    return


@app.cell
def _(json, country_data):
    chart_data = [{"n": c if c != "Korea, Rep." else "South Korea", "pts": pts2} for c, pts2 in sorted(country_data.items())]
    print(json.dumps(chart_data))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
