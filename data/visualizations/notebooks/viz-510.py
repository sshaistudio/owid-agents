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
        # Private Health Expenditure — Methodology

        Documents the data pipeline behind viz-510.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-XPD-PVTD-CH-ZS.json"
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
                    'states', 'development', 'South Asia', 'FCV', 'Conflict']
    v2000 = {}
    v2022 = {}
    for r in data:
        c = r['countryName']
        if any(kw.lower() in c.lower() for kw in agg_keywords):
            continue
        if r['value'] is None:
            continue
        if r['year'] == 2000:
            v2000[c] = r['value']
        elif r['year'] == 2022:
            v2022[c] = r['value']
    common = set(v2000) & set(v2022)
    print(f"Countries with 2000 and 2022 data: {len(common)}")
    return agg_keywords, common, v2000, v2022


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — compare 2000 vs 2022 to show direction of change
        - **Country selection**: Mix of high-private-spending (low-income), mid-range, and low-private-spending
          (strong public systems) countries
        - **Color**: Direction and magnitude of change; red = more private (worse access), green = less private (better)
        - **Story**: India made progress (76% → 58%); Armenia went backwards (65% → 82%)
        """
    )
    return


@app.cell
def _(json, common, v2000, v2022):
    pairs = [(c, round(v2000[c], 1), round(v2022[c], 1)) for c in common]
    pairs.sort(key=lambda x: -x[2])
    chart_data = [{"n": c, "a": a, "b": b} for c, a, b in pairs[:10]] + \
                 [{"n": c, "a": a, "b": b} for c, a, b in [
                     ("India", round(v2000["India"], 1), round(v2022["India"], 1)),
                     ("Cambodia", round(v2000["Cambodia"], 1), round(v2022["Cambodia"], 1)),
                     ("Georgia", round(v2000["Georgia"], 1), round(v2022["Georgia"], 1)),
                     ("China", round(v2000["China"], 1), round(v2022["China"], 1)),
                     ("Brazil", round(v2000["Brazil"], 1), round(v2022["Brazil"], 1)),
                     ("South Africa", round(v2000["South Africa"], 1), round(v2022["South Africa"], 1)),
                     ("Mexico", round(v2000["Mexico"], 1), round(v2022["Mexico"], 1)),
                     ("Turkey", round(v2000["Turkey"], 1), round(v2022["Turkey"], 1)),
                     ("Poland", round(v2000["Poland"], 1), round(v2022["Poland"], 1)),
                     ("Japan", round(v2000["Japan"], 1), round(v2022["Japan"], 1)),
                     ("Germany", round(v2000["Germany"], 1), round(v2022["Germany"], 1)),
                     ("France", round(v2000["France"], 1), round(v2022["France"], 1)),
                     ("Denmark", round(v2000["Denmark"], 1), round(v2022["Denmark"], 1)),
                     ("Czechia", round(v2000["Czechia"], 1), round(v2022["Czechia"], 1)),
                     ("United Kingdom", round(v2000["United Kingdom"], 1), round(v2022["United Kingdom"], 1)),
                 ] if c in v2000 and c in v2022]
    seen = set()
    unique = []
    for item in chart_data:
        if item["n"] not in seen:
            seen.add(item["n"])
            unique.append(item)
    unique.sort(key=lambda x: -x["b"])
    print(json.dumps(unique, separators=(",", ":")))
    return chart_data, pairs, seen, unique


if __name__ == "__main__":
    app.run()
