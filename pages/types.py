import dash
from dash import html

dash.register_page(__name__, path='/types')

layout = html.Div([
    html.H1('Chloe - page des flowchart des types')
])