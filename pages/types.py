import dash
from dash import html, dcc 
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import dash_cytoscape as cyto



import pandas as pd
import yaml
import os

dash.register_page(__name__, path='/types')

type_link = {
    "normal": "https://archives.bulbagarden.net/media/upload/0/08/NormalIC_SV.png",
    "fighting": "https://www.pokepedia.fr/Fichier:Miniature_Type_Combat_GO.png",
    "flying": "https://archives.bulbagarden.net/media/upload/d/d7/FlyingIC_SV.png",
    "poison": "https://archives.bulbagarden.net/media/upload/9/9d/PoisonIC_SV.png",
    "ground": "https://archives.bulbagarden.net/media/upload/f/f8/GroundIC_SV.png",
    "rock": "https://archives.bulbagarden.net/media/upload/3/32/RockIC_SV.png",
    "bug": "https://archives.bulbagarden.net/media/upload/d/d1/BugIC_SV.png",
    "ghost": "https://archives.bulbagarden.net/media/upload/2/2c/GhostIC_SV.png",
    "steel": "https://www.pokepedia.fr/Fichier:Miniature_Type_Acier_GO.png",
    "fire": "https://archives.bulbagarden.net/media/upload/a/a2/FireIC_SV.png",
    "water": "https://archives.bulbagarden.net/media/upload/d/de/WaterIC_SV.png",
    "grass": "https://archives.bulbagarden.net/media/upload/7/7b/GrassIC_SV.png",
    "electric": "https://archives.bulbagarden.net/media/upload/7/77/ElectricIC_SV.png",
    "psychic": "https://archives.bulbagarden.net/media/upload/1/13/IceIC_SV.png",
    "ice": "https://archives.bulbagarden.net/media/upload/9/96/PsychicIC_SV.png",
    "dragon": "https://archives.bulbagarden.net/media/upload/7/7f/DragonIC_SV.png",
    "dark": "https://archives.bulbagarden.net/media/upload/3/30/DarkIC_SV.png",
    "fairy": "https://archives.bulbagarden.net/media/upload/c/c6/FairyIC_SV.png"
}

comment = html.Div(style={'color': 'dark'},
                   children=[
                       html.P("""
    Arrows represent the effectiveness of a type against another. 
                              """),
                        html.Ul(children=[
                            html.Li("Green arrow : the type is super effective"),
                            html.Li("Black arrow : the type is not very effective"),
                            html.Li("Red arrow : the type is not effective")
                        ])
                   ])

# Load data from a YAML file
with open(os.path.join('data', 'type-chart.yaml'), 'r') as file:
    data = yaml.safe_load(file)

type_chart = pd.DataFrame(data).T

weights = {"super-effective": 2, "not-very-effective": 0.5, "no-effect": 0}
nodes = [{ "data" : {"id" : label, 
                     "label" : label.capitalize(),
                     'url': 'https://www.pokepedia.fr/images/c/c8/Miniature_Type_Acier_GO.png'}
                     } for label in type_chart.index]

col_eff = {
    "not-very-effective" : "red",
    "no-effect" : "black",
    "super-effective" : "green"
}

edges = []
for source in type_chart.index:
    for efficiency in type_chart:
        for target in type_chart.at[source,efficiency]:
            edges.append({"data": {"source": source, 
                                   "target": target, 
                                   "efficiency":efficiency, 
                                   "color" : col_eff[efficiency] }})
elements = nodes + edges

stylesheet = [
                {
                    'selector' : '[efficiency = "no-effect"]',
                    'style':{
                        'curve-style' : 'bezier',
                        'source-arrow-color': 'yellow',
                        'source-arrow-shape': 'triangle',
                        'line-color':'data(color)'
                    }
                },
                {
                    'selector' : '[efficiency = "not-very-effective"]',
                    'style':{
                        'curve-style' : 'bezier',
                        'source-arrow-color': 'pink',
                        'source-arrow-shape': 'triangle',
                        'line-color':'data(color)'
                    }
                },
                {
                    'selector' : '[efficiency = "super-effective"]',
                    'style':{
                        'curve-style' : 'bezier',
                        'source-arrow-color': 'purple',
                        'source-arrow-shape': 'triangle',
                        'line-color':'data(color)'
                    }
                },
                {
                    'selector': 'node',
                    'style' : {'label': 'data(label)',
                                'width': 50,
                                'height': 50,
                                'background-fit': 'cover',
                                'background-image': 'data(url)'
                                
                    }
                }
            ]

layout = html.Div([
    html.H1('Effectiveness of types'),
        dcc.Dropdown(
            id="dropdown-update-layout",
            value="circle",
            clearable=False,
            options=[
                {"label": name.capitalize(), "value": name}
                for name in ["grid", "random", "circle", "cose", "concentric"]
            ],
        ),
        cyto.Cytoscape(
            id="cytoscape-update-layout",
            layout={"name": "grid"},
            style={"width": "100%", "height": "900px"},
            elements=edges + nodes,
            stylesheet= stylesheet
        ),
    comment
    ]
)


@dash.callback(
    Output("cytoscape-update-layout", "layout"),
    Input("dropdown-update-layout", "value")
)
def update_layout(layout):
    
    return {"name": layout, "animate": True}