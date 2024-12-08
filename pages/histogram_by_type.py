import dash
from dash import html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import numpy as np
from load_dataset import pokemon_dataset, preprocessed_dataset
from sklearn.manifold import TSNE
final_df = preprocessed_dataset()
raw_df = pokemon_dataset()

dash.register_page(__name__, path='/histogram')

commment = html.Div(style={"color" : "dark"},
                    children=[
    html.P("""On this graph, you can observe the repartition of the values 
           from the dropdown feature by types, either compare multiple types 
           or a single one""")
])

layout = html.Div([
        ## Histogram
    html.H1(" Histogram of the distribution of values of a feature by type "),
    html.Hr(),
    #dcc.Checklist(raw_df["type1"].unique(),
    #             value=["Normal"],
    #             id="hist-types"),
    dcc.Dropdown(raw_df.columns,
                  value="hp",
                  id="hist-x"),
    dcc.Graph(figure={}, id="hist-by-type"),
    commment

])



@callback(
    Output("hist-by-type", "figure"),
    #Input("hist-types", "value"),
    Input("hist-x", "value")
)
def hist_by_type( values_x):
    """HIST BY TYPE
    
    Keyword arguments:
    TYPES -- Types to display
    values_x -- x-axis values
    values_y -- y-axis values
    Return: histogram
    """
    
    fig = px.histogram(raw_df,
                       x=values_x,
                       color='type1',
                       barmode="group")
    return fig