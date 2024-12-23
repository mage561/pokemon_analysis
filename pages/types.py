import dash
from dash import html, dcc 
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import dash_cytoscape as cyto



import pandas as pd
import yaml
import os

dash.register_page(__name__, path='/types')

# Load data from a YAML file
with open(os.path.join('data', 'type-chart.yaml'), 'r') as file:
    data = yaml.safe_load(file)

type_chart = pd.DataFrame(data).T

weights = {"super-effective": 2, "not-very-effective": 0.5, "no-effect": 0}
nodes = [{ "data" : {"id" : label, "label" : label} } for label in type_chart.index]

col_eff = {
    "not-very-effective" : "blue",
    "no-effect" : "red",
    "super-effective" : "green"
}

edges = []
for source in type_chart.index:
    for efficiency in type_chart:
        for target in type_chart.at[source,efficiency]:
            edges.append({"data": {"source": source, "target": target, "efficiency":efficiency, "color" : col_eff[efficiency] }})
elements = nodes + edges



layout = html.Div([
    html.H1('Chloe - page des flowchart des types'),
        dcc.Dropdown(
            id="dropdown-update-layout",
            value="grid",
            clearable=False,
            options=[
                {"label": name.capitalize(), "value": name}
                for name in ["grid", "random", "circle", "cose", "concentric"]
            ],
        ),
        cyto.Cytoscape(
            id="cytoscape-update-layout",
            layout={"name": "grid"},
            style={"width": "100%", "height": "450px"},
            elements=edges + nodes,
            stylesheet=[
                {
                    'selector' : 'edge',
                    'style':{
                        'source-arrow-color': 'data(color)',
                        'source-arrow-shape': 'triangle',
                        'line-color':'data(color)'
                    }
                },
                {
                    'selector': 'node',
                    'style' : {'label': 'data(label)'
                    }
                }
            ]
        ),
        dcc.Checklist(
            id='nodes-show',
            options=list(type_chart.index),
            value= type_chart.index,
            inline=True,
        )
    ]
)


@dash.callback(
    Output("cytoscape-update-layout", "layout"),
    Input("dropdown-update-layout", "value"),
    Input('nodes-show', "value")
)
def update_layout(layout, dropdown_layout, nodes_to_show):
    
    return {"name": layout, "animate": True, "nodes_to_show": nodes_to_show}