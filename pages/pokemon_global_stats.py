import dash
from dash import html

dash.register_page(__name__, path='/pkm_global')

layout = html.Div([
    html.H1('Chloe - display the big tsne on all dimansion and all stat')
])