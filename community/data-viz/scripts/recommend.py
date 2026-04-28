#!/usr/bin/env python3
"""data-viz recommend — pick a chart type + emit starter code."""
import argparse, json, sys

LIBS = {
    "recharts": "https://recharts.org",
    "echarts":  "https://echarts.apache.org",
    "vega-lite":"https://vega.github.io/vega-lite/",
    "d3":       "https://d3js.org",
    "plot":     "https://observablehq.com/plot/",
    "matplotlib":"https://matplotlib.org",
}

DECISION = {
    "compare":   ["bar", "dot-plot"],
    "trend":     ["line", "area"],
    "distribution": ["histogram", "violin", "boxplot"],
    "composition":  ["stacked-bar", "treemap"],
    "relation":  ["scatter", "hexbin"],
    "ranking":   ["sorted-bar", "bump"],
    "flow":      ["sankey", "chord"],
    "geo":       ["choropleth", "hex-grid"],
    "network":   ["force-graph", "adjacency-matrix"],
}

STARTERS = {
("recharts","line"): """import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
export default function Chart({data}) {
  return (<ResponsiveContainer width="100%" height={300}>
    <LineChart data={data}>
      <XAxis dataKey="x" /><YAxis /><Tooltip />
      <Line type="monotone" dataKey="y" stroke="#0ea5e9" />
    </LineChart>
  </ResponsiveContainer>);
}""",
("recharts","bar"): """import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
export default function Chart({data}) {
  return (<ResponsiveContainer width="100%" height={300}>
    <BarChart data={data}><XAxis dataKey="x" /><YAxis /><Tooltip />
      <Bar dataKey="y" fill="#0ea5e9" /></BarChart>
  </ResponsiveContainer>);
}""",
("vega-lite","scatter"): """{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {"url": "data.csv"},
  "mark": "point",
  "encoding": {"x": {"field":"x","type":"quantitative"},
               "y": {"field":"y","type":"quantitative"}}
}""",
("plot","histogram"): """import * as Plot from "@observablehq/plot";
Plot.plot({marks:[Plot.rectY(data, Plot.binX({y:"count"}, {x:"value"}))]})""",
}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--intent", choices=list(DECISION),
                   help="compare/trend/distribution/composition/relation/ranking/flow/geo/network")
    p.add_argument("--library", default="recharts", choices=list(LIBS))
    p.add_argument("--rows", type=int)
    p.add_argument("--x-type", choices=["cat","num","time"])
    p.add_argument("--y-type", choices=["num"])
    args = p.parse_args()

    # auto infer if intent missing
    if not args.intent:
        if args.x_type == "time": args.intent = "trend"
        elif args.x_type == "cat" and args.y_type == "num": args.intent = "compare"
        else: args.intent = "relation"

    chart_options = DECISION[args.intent]
    chart = chart_options[0]

    # If rows huge + scatter → suggest hexbin
    if chart == "scatter" and args.rows and args.rows > 5000:
        chart = "hexbin"

    starter = STARTERS.get((args.library, chart))
    out = {
      "intent": args.intent,
      "recommended_chart": chart,
      "alternatives": chart_options[1:],
      "library": args.library,
      "library_docs": LIBS[args.library],
      "starter_code": starter or f"# no starter for {args.library}+{chart}, see {LIBS[args.library]}",
      "checklist": [
        "axis labels w/ units",
        "color-blind safe palette (Okabe-Ito / viridis)",
        "legend if multi-series",
        "WCAG 3:1 contrast",
        "tooltip / a11y description",
      ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
