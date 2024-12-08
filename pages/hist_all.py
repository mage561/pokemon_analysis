import dash
from dash import html

dash.register_page(__name__, path='/histogram')

layout = html.Div([
    html.H1('Chloe - Histogram for everything')
])