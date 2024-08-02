import dash
from dash import dcc, html, Input, Output, callback
import polars as pl
import dash_bootstrap_components as dbc
from dash_ag_grid import AgGrid
import dash_mantine_components as dmc
from db import Task

df= Task()


column_defs = [
    {"headerName": "ID", "field": "ID"},
    {"headerName": "TASK", "field": "Task"},
    {"headerName": "DESCRIPTION", "field": "Description"},
    {"headerName": "TYPE", "field": "Type"},
    {"headerName": "STATUS", "field": "Status"},
    {"headerName": "LOCATION", "field": "Location"},
    {"headerName": "ORG", "field": "ORG"}
]

dash.register_page(__name__, path='/')


layout = dmc.MantineProvider(
    children=[
        html.Div([
            dbc.Row([
                dbc.Col(dcc.Dropdown(
                    id='location-dropdown',
                    options=[{'label': loc, 'value': loc} for loc in df['Location'].unique()],
                    placeholder='Location',
                    multi=True,
                    className="custom-dropdown",
                    style={'background-color': 'transparent'}
                )),
                dbc.Col(dcc.Dropdown(
                    id='type-dropdown',
                    options=[{'label': task_type, 'value': task_type} for task_type in df['Type'].unique()],
                    placeholder='Task Type',
                    multi=True,
                    className="custom-dropdown",
                    style={'background-color': 'transparent'}
                ))
            ]),
            dmc.Grid(
                children=[
                    dmc.GridCol(html.Div([
                        html.H4("Total Tasks"),
                        html.H2(id='total-tasks', className='task-count')
                    ], className='card'), span=3),
                    dmc.GridCol(html.Div([
                        html.H4("Completed Tasks"),
                        html.H2(id='completed-tasks', className='task-count')
                    ], className='card'), span=3),
                    dmc.GridCol(html.Div([
                        html.H4("Pending Tasks"),
                        html.H2(id='pending-tasks', className='task-count')
                    ], className='card'), span=3),
                    dmc.GridCol(html.Div([
                        html.H4("Inspected Tasks"),
                        html.H2(id='inspected-tasks', className='task-count')
                    ], className='card'), span=3),
                ],
            ),
            html.Div([
                AgGrid(className="ag-theme-alpine",
                    defaultColDef={"resizable": False,"filter": True},
                    columnSize="sizeToFit",
                    id='task-table',
                    columnDefs=column_defs,
                    rowData=[],
                    rowStyle = {"backgroundColor": "white", "color": "Black"},
                    style={'height': '65vh', 'width': '100%', 'text-align': 'center'},
                    dashGridOptions={"rowHeight": 60
            }
                )
            ])
        ])
    ]
)

@callback(
    [
        Output('total-tasks', 'children'),
        Output('completed-tasks', 'children'),
        Output('pending-tasks', 'children'),
        Output('inspected-tasks', 'children'),
        Output('task-table', 'rowData')
    ],
    [
        Input('organization-id-store', 'data'),
        Input('location-dropdown', 'value'),
        Input('type-dropdown', 'value')
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
