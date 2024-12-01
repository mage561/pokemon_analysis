import dash
from dash import html

dash.register_page(__name__, path='/pkm_indiv')

layout = html.Div([
    html.H1('Pitou - display 1 pokemon à la fois + la liste')
])