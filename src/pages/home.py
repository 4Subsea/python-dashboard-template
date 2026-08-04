"""
Landing page
------------

This is the "Home" page, which is the first page users see when they open the app.
It contains a table of sample data fetched from the "assets/sample_data.csv" file.
The table is implemented using the Dash AG Grid component, which allows for filtering, sorting, and pagination.

"""

import pathlib

import dash
import dash_ag_grid as dag
import pandas as pd
from dash import dcc, html

dash.register_page(__name__, path="/", name="Home", order=0)

SAMPLE_DATA_PATH = pathlib.Path(__file__).resolve().parents[1] / "assets" / "sample_data.csv"


def load_sample_data():
    """Not shared with app.py: importing from app here would re-trigger Dash's
    own page auto-discovery when the app is run as a script. See analytics.py
    for the same function - duplicated rather than imported, on purpose."""
    return pd.read_csv(SAMPLE_DATA_PATH)


def layout():
    df = load_sample_data()
    grid = dag.AgGrid(
        id="home-sample-grid",
        rowData=df.to_dict("records"),
        columnDefs=[{"field": col, "headerName": col} for col in df.columns],
        defaultColDef={"filter": True, "sortable": True},
        columnSize="responsiveSizeToFit",
        dashGridOptions={
            "theme": "themeBalham",
            "animateRows": True,
            "pagination": True,
            "paginationPageSize": 10,
        },
    )
    return html.Div(
        [
            html.Div(
                [
                    dcc.Markdown(
                        "Replace this page, `src/assets/sample_data.csv` and the "
                        "example on the Analytics page with your own."
                    ),
                ],
                className="visual",
            ),
            html.Div(
                [
                    html.Div("Sample data", className="visual-title"),
                    dcc.Loading(grid),
                ],
                className="visual",
            ),
        ]
    )
