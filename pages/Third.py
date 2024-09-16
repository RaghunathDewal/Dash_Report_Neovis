import dash
from dash import dcc, html, Input, Output, callback
import polars as pl
from DB.queries import get_employee_date
import dash_bootstrap_components as dbc
from dash_ag_grid import AgGrid
import dash_mantine_components as dmc
from DB.db import DB

# Load data
df = get_employee_date()

dash.register_page(__name__, path="/Employee")

column_defs = [{"headerName": col, "field": col} for col in df.columns if col != "ORG"]

layout = dmc.MantineProvider(
    children=[
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Dropdown(
                                id="location-dropdown-Third",
                                options=[
                                    {"label": loc, "value": loc}
                                    for loc in df["Location"].unique()
                                ],
                                placeholder="Location",
                                multi=True,
                                className="custom-dropdown",
                                style={'width':'50vh','padding-bottom': '10px'}
                            )
                        ),
                    ]
                ),
                html.Div(
                    [
                        AgGrid(
                            className="ag-theme-alpine",
                            defaultColDef={"resizable": False},
                            columnSize="sizeToFit",
                            id="Employee_table",
                            columnDefs=column_defs,
                            rowData=[],
                            rowStyle={"backgroundColor": "white", "color": "Black"},
                            style={
                                "height": "67vh",
                                "width": "100%",
                                "text-align": "center",
                            },
                            dashGridOptions={
                                "rowHeight": 60,
                            },
                        )
                    ]
                ),
            ]
        )
    ]
)


@callback(
    [
        Output("Employee_table", "rowData"),
    ],
    [
        Input("organization-id-store", "data"),
        Input("location-dropdown-Third", "value"),
    ],
)
def update_scorecards(organization_id, selected_locations):
    filtered_df = df

    if organization_id:
        try:
            organization_id = int(organization_id)
            filtered_df = filtered_df.filter(pl.col("ORG") == organization_id)
        except ValueError:
            print(f"Invalid organization_id: {organization_id}")

    if selected_locations:
        filtered_df = filtered_df.filter(pl.col("Location").is_in(selected_locations))


    row_data = filtered_df.to_dicts()

    return (
        row_data,
    )
