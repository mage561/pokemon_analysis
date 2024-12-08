import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True,
           external_stylesheets=[dbc.themes.CERULEAN])

nav = dbc.Nav(
    class_name="navbar navbar-expand-lg bg-primary", style={'data-bs-theme' : 'dark'},
    children = [ 
       
        dbc.NavItem(
            dbc.Button(f"{page['name']}", 
                        active=True, 
                        href=page["relative_path"]))
                    for page in dash.page_registry.values()
    ],
    pills=False,
    )
classic = html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", 
                     href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ])



footer = html.Div(
    className="footer",
    children=[
        html.P("Pokémon Analysis Dash App © Automn 2024"),
        html.P("Created by Pierre-Antoine NAVARRO and Chloé LADREYT"),

    ],
    style={
        'textAlign': 'center',
        'padding': '1rem',
        #'backgroundColor': '#007bff',
        'color': '#007bff'
    }
)

app.layout = html.Div(style = {'color': 'dark', "fontSize" : 15},
    children=[
        html.Header('Présentation des pokémons et leur caractéristiques'),
        nav,
        dash.page_container,
        footer
])



if __name__ == '__main__':
    app.run(debug=True)