import dash
from dash import html
import dash_leaflet as dl

def open_map(positions):
    markers = [dl.Marker(dl.Tooltip(key), position=value, id="marker{}".format(key)) for key, value in positions.items()]
    cluster = dl.MarkerClusterGroup(id="markers", children=markers, options={"polygonOptions": {"color": "green"}})

    app = dash.Dash(prevent_initial_callbacks=True)
    app.layout = html.Div([
        html.Div(dl.Map([dl.TileLayer(), cluster], center=(33, 33), zoom=3, id="map",
                        style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"})),
        html.Div(id='clickdata')
    ])


    app.run_server()

