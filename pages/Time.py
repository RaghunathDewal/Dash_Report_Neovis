import dash
from dash import dcc, html, Input, Output, callback
import polars as pl
from DB.queries import Time
import dash_bootstrap_components as dbc
from dash_ag_grid import AgGrid
import dash_mantine_components as dmc
from DB.db import DB
# Load data
df = Time()
DB.close_connection_pool()
dash.register_page(__name__, path='/time')

column_defs = [{"headerName": col, "field": col} for col in df.columns if col != 'ORG']

layout = dmc.MantineProvider(
    children=[
        html.Div([
            dbc.Row([
                dbc.Col(dcc.Dropdown(
    id='location-dropdown-Time',
    options=[{'label': loc, 'value': loc} for loc in df['Location'].unique()],
    placeholder='Location',
    multi=True,
    className="custom-dropdown")),           
                dbc.Col(dcc.Dropdown(
                    id='type-dropdown-Time',
                    options=[{'label': task_type, 'value': task_type} for task_type in df['Type'].unique()],
                    placeholder='Task Type',
                    multi=True,
                    className="custom-dropdown"
                ))
            ]),
            dmc.Grid(
                children=[
                    dmc.GridCol(html.Div([
                        html.H4("Total Tasks"),
                        html.H2(id='total-tasks-Time',)
                    ], className='card'), span=3),
                    dmc.GridCol(html.Div([
                        html.H4("Completed Tasks"),
                        html.H2(id='completed-tasks-Time',)
                    ], className='card'), span=3),
                    dmc.GridCol(html.Div([
                        html.H4("Pending Tasks"),
                        html.H2(id='pending-tasks-Time',)
                    ], className='card'), span=3),
                    dmc.GridCol(html.Div([
                        html.H4("Inspected Tasks"),
                        html.H2(id='inspected-tasks-Time',)
                    ], className='card'), span=3),
                ],
            ),
            html.Div([
                AgGrid(className="ag-theme-alpine",
                    defaultColDef={"resizable": True},
                    columnSize="sizeToFit",
                    id='task-table-Time',
                    columnDefs=column_defs,
                    rowData=[],
                    rowStyle = {"backgroundColor": "white", "color": "Black"},
                    style={'height': '65vh', 'width': '100%', 'text-align': 'center'},
                    dashGridOptions={"rowHeight": 60,
            }
                )
            ])
        ])
    ]
)

@callback(
    [
        Output('total-tasks-Time', 'children'),
        Output('completed-tasks-Time', 'children'),
        Output('pending-tasks-Time', 'children'),
        Output('inspected-tasks-Time', 'children'),
        Output('task-table-Time', 'rowData')
    ],
    [
        Input('organization-id-store', 'data'),
        Input('location-dropdown-Time', 'value'),
        Input('type-dropdown-Time', 'value')
    ]
)
def update_scorecards(organization_id, selected_locations, selected_types):
    filtered_df = df

    
    if organization_id:
        try:
            organization_id = int(organization_id)  
            filtered_df = filtered_df.filter(pl.col('ORG') == organization_id)
        except ValueError:
            print(f"Invalid organization_id: {organization_id}")

   
    if selected_locations:
        filtered_df = filtered_df.filter(pl.col('Location').is_in(selected_locations))

    if selected_types:
        filtered_df = filtered_df.filter(pl.col('Type').is_in(selected_types))


    total_tasks = filtered_df.shape[0]
    completed_tasks = filtered_df.filter(pl.col('Status') == 'Completed').shape[0]
    pending_tasks = filtered_df.filter(pl.col('Status') == 'Pending').shape[0]
    inspected_tasks = filtered_df.filter(pl.col('Status') == 'Inspected').shape[0]

    row_data = filtered_df.to_dicts()

    return (
        f"{total_tasks}",
        f"{completed_tasks}",
        f"{pending_tasks}",
        f"{inspected_tasks}",
        row_data
    )