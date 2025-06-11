import dash
from dash import Dash, html, dcc, callback, Input, Output, State
import dash_mantine_components as dmc
from urllib.parse import urlparse, parse_qs, urlencode


def get_icon_from_assets(icon_filename):
    return html.Img(src=f"/assets/{icon_filename}")


external_css = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css"
]
app = Dash(__name__, use_pages=True, external_stylesheets=external_css)
server = app.server

app.layout = dmc.MantineProvider(
    html.Div(
        [
            dcc.Location(id="url", refresh=False),
            dcc.Store(id="organization-id-store", storage_type="session", data=None),
            html.Div(
                className="dashboard-container",
                children=[
                    html.Nav(
                        className="sidebar",
                        children=[
                            dcc.Link(
                                html.Img(className="logoimg2",style={'margin-top':'13px'}, src="/assets/ICON.png"),
                                href="/",
                            ),
                            dmc.Tooltip(
                                label="Go to Home",
                                position="right",
                                children=dmc.NavLink(
                                    
                                    href="/",
                                    leftSection=get_icon_from_assets(
                                        "bi--house-door-fill.svg"
                                    ),
                                ),
                            ),
                            dmc.Tooltip(
                                label="View Time Report",
                                position="right",
                                children=dmc.NavLink(
                                    href="/time",
                                    leftSection=get_icon_from_assets(
                                        "mdi--clock-outline.svg"
                                    ),
                                ),
                            ),
                            dmc.Tooltip(
                                label="Check Employee Rating",
                                position="right",
                                children=dmc.NavLink(
                                    href="/Employee",
                                    leftSection=get_icon_from_assets(
                                        "mdi--clock-outline.svg"
                                    ),
                                ),
                            ),
                        ],
                    ),
                    html.Main(
                        className="main-content",
                        children=[
                            html.Header(
                                className="header",
                                children=[
                                    dcc.Link(
                                        html.Img(
                                            className="logoimg",
                                            src="/assets/NAME.png",
                                        ),
                                        href="/",
                                    )
                                ],
                            ),
                            html.Div(
                                className="content", children=[dash.page_container]
                            ),
                            html.Footer(
                                className="footer",
                                children=[
                                    html.Div(
                                        children=[
                                            dcc.Link(
                                                html.Img(
                                                    className="logoimg",
                                                    src="/assets/NAME.png",
                                                ),
                                                href="/",
                                            )
                                        ]
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )
)


@app.callback(
    Output("organization-id-store", "data"),
    Input("url", "href"),
    State("organization-id-store", "data"),
)
def set_organization_id(href, current_org_id):
    if current_org_id is None and href:
        parsed_url = urlparse(href)
        query_params = parse_qs(parsed_url.query)
        org_id = query_params.get("organization_id", [None])[0]
        return org_id
    return current_org_id


@app.callback(
    Output("url", "href"), Input("url", "href"), State("organization-id-store", "data")
)
def ensure_correct_organization_id(href, stored_org_id):
    if href and stored_org_id:
        parsed_url = urlparse(href)
        query_params = parse_qs(parsed_url.query)
        url_org_id = query_params.get("organization_id", [None])[0]

        if url_org_id != stored_org_id:
            query_params["organization_id"] = [stored_org_id]
            new_query = urlencode(query_params, doseq=True)
            new_url = parsed_url._replace(query=new_query).geturl()
            return new_url
    return href
if __name__ == "__main__":
    app.run_server(debug=False)


if __name__ == "__main__":
    app.run_server(debug=False)
