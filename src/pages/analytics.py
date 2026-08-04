"""Analytics page: one slicer, one chart, server-side filtering.

Minimal example of a filter driving a Plotly figure. The figure gets its
styling for free from the "4subsea" template theme.py registers as Plotly's
default on import - nothing here sets a colour or a font.
"""

import pathlib

import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, callback, dcc, html

dash.register_page(__name__, path="/analytics", name="Analytics", order=1)

SAMPLE_DATA_PATH = pathlib.Path(__file__).resolve().parents[1] / "assets" / "sample_data.csv"


def load_sample_data():
    """Not shared with app.py: importing from app here would re-trigger Dash's
    own page auto-discovery when the app is run as a script. See home.py for
    the same function - duplicated rather than imported, on purpose."""
    return pd.read_csv(SAMPLE_DATA_PATH)


def layout():
    df = load_sample_data()
    categories = sorted(df["category"].unique())
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Category", className="slicer-header"),
                    dcc.Dropdown(
                        id="analytics-category-filter",
                        options=[{"label": c, "value": c} for c in categories],
                        value=categories[0],
                        clearable=False,
                    ),
                ],
                className="slicer",
            ),
            html.Div(
                [
                    html.Div("Value vs. target over time", className="visual-title"),
                    dcc.Loading(dcc.Graph(id="analytics-chart")),
                ],
                className="visual",
            ),
        ]
    )


# Callback to update the chart based on the selected category. Note that the callback is a decorator that takes the output and input components as arguments. The function itself takes the input value and returns the updated figure.
@callback(
    Output("analytics-chart", "figure"),
    Input("analytics-category-filter", "value"),
)
def update_chart(category):
    # Filtered in Python before it reaches the figure, rather than sending the
    # whole dataset to the client and filtering there.
    df = load_sample_data()
    filtered = df[df["category"] == category]
    return px.line(
        filtered,
        x="date",
        y=["value", "target"],
        labels={"value": "Amount", "variable": ""},
    )
