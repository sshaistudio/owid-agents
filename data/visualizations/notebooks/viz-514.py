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
    # Current Account Balance — Methodology

    Trend lines showing current account balance (% of GDP) for 6 economies
    from 1990 to 2024, illustrating persistent global trade imbalances.
    """)
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
    sel_countries = ["Australia", "Brazil", "China", "France", "Germany", "Canada"]
    pts = [p for p in data if p["value"] is not None and p["countryName"] in sel_countries and p["year"] >= 1990]
    country_data = {}
    for p in pts:
        c = p["countryName"]
        if c not in country_data:
            country_data[c] = []
        country_data[c].append({"y": p["year"], "v": round(p["value"], 2)})
    for c in country_data:
        country_data[c].sort(key=lambda x: x["y"])
        first = country_data[c][0]
        last = country_data[c][-1]
        print(f"{c}: {first['v']:+.1f}% ({first['y']}) -> {last['v']:+.1f}% ({last['y']})")
    return country_data, pts, sel_countries


@app.cell
def _(mo):
    mo.md("""
    ## Design Rationale

    - **Chart type**: Trend lines with zero reference line — shows surplus vs deficit clearly
    - **Country selection**: 6 economies showing contrasting trajectories (Germany surplus,
      Australia deficit, China peaked in 2007)
    - **Time range**: 1990–2024
    - **Highlights**: Germany's surplus grew from near-zero in 2000 to nearly 9% of GDP
      by 2016; China's surplus peaked at ~10% in 2007 and has since contracted;
      Australia ran persistent deficits until a commodity boom briefly pushed it positive
    """)
    return


@app.cell
def _(json, country_data):
    chart_data = [{"n": c, "pts": pts2} for c, pts2 in sorted(country_data.items())]
    print(json.dumps(chart_data))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
