"""Home page: revision log and a free-text notes box.

Landing page. The revision log records who issued, checked and approved
each version of the app's content - add a row to issue a new revision
rather than editing the last one, since the point of the log is the
history.
"""

import dash
import dash_ag_grid as dag
from dash import dcc, html

dash.register_page(__name__, path="/", name="Home", order=0)

# Empty Checked, Approved, etc. mean exactly that: not yet checked, not yet
# approved. Fill them in when you fill in a real revision.

REVISION_LOG = [
    {
        "Revision No.": "1.0",
        "Date": "2026-01-01",
        "Author": "ABC",
        "Checked": "DEF",
        "Approved": "GHI",
        "Reason for issue": "Issued for client review",
    },
]


def layout():
    grid = dag.AgGrid(
        id="home-revision-log-grid",
        rowData=REVISION_LOG,
        # headerName explicitly, or AG Grid title-cases the field: "Reason for
        # issue" would render as "Reason For Issue".
        columnDefs=[{"field": col, "headerName": col} for col in REVISION_LOG[0]],
        defaultColDef={"filter": True, "sortable": True},
        columnSize="responsiveSizeToFit",
        dashGridOptions={
            "theme": "themeBalham",
            "animateRows": True,
            # No pagination: the log only ever holds a handful of rows, and
            # autoHeight sizes the grid to its content instead of drawing a
            # tall empty box with a pager underneath it.
            "pagination": False,
            "domLayout": "autoHeight",
            # A dot in a field name is a nested-property path to AG Grid, so
            # "Revision No." would look up row["Revision No"][""] and render
            # blank. The field names here are human labels, never paths.
            "suppressFieldDotNotation": True,
        },
    )
    return html.Div(
        [
            
            html.Div(
                dcc.Textarea(
                    id="home-notes-textarea",
                    value="Here you can write free-text notes about the app's content, or anything else you want to remember.",
                    className="notes-textarea",
                ),
                className="visual",
            ),
            html.Div(
                            [
                                html.Div("Revision log", className="visual-title"),
                                dcc.Loading(grid),
                            ],
                            className="visual row-gap",
                        )
        ],
        # A small table and a text box read as mostly whitespace spread
        # across the full 1800px content width.
        className="narrow-page",
    )
