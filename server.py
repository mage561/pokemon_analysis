# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from load_dataset import pokemon_dataset, preprocessed_dataset
from plots_gen import pokemon_tsne, hist_by_type

app = Dash()

app.layout=html.Div(children=[html.H1("Pokemon TSNE"),
    html.Hr(),
    dcc.RadioItems(options =pokemon_dataset().columns, 
                    value="type1", 
                    id="color-col"),
    dcc.Slider(5, 50,  step = 5, 
               value = 30,
               id="perplex-slider"),
    dcc.Graph(figure={}, id="tsne-graph")
    ])



@callback(Output(component_id="tsne-graph", component_property="figure"),
    Input(component_id="color-col", component_property="value"),
    Input(component_id="perplex-slider", component_property="value")
    
)
def poke_tsne(color_column, perplexity):
    return pokemon_tsne(color_column, perplexity)

if __name__ == '__main__':
    app.run(debug=True)