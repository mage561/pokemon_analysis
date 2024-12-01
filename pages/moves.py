import dash
from dash import html

dash.register_page(__name__, path='/moves')

layout = html.Div([
    html.H1('Pitou - pages des tsne etc pour les moves')
])