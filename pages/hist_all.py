import dash
from dash import html
# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from load_dataset import pokemon_dataset, preprocessed_dataset
import numpy as np
#from plots_gen import pokemon_tsne, hist_by_type, scatter_everything
from sklearn.manifold import TSNE
final_df = preprocessed_dataset()
raw_df = pokemon_dataset()

dash.register_page(__name__, path='/histogram')

layout = html.Div([
        ## Histogram
    html.H1(" Histogram by type "),
    html.Hr(),
    #dcc.Checklist(raw_df["type1"].unique(),
    #             value=["Normal"],
    #             id="hist-types"),
    dcc.Dropdown(raw_df.columns,
                  value="hp",
                  id="hist-x"),
    dcc.Graph(figure={}, id="hist-by-type"),


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