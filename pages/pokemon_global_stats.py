import dash
from dash import html, dcc
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

dash.register_page(__name__, path='/pkm_global')

layout = html.Div([
 
    # TSNE
    html.H1("Pokemon TSNE global"),
    html.Hr(),
    dcc.Dropdown(options =raw_df.columns, 
                    value="type1", 
                    id="color-col"),
    dcc.Slider(5, 50,  step = 5, 
               value = 30,
               id="perplex-slider"),
    dcc.Graph(figure={}, id="tsne-graph")

])


@callback(
    Output(component_id="tsne-graph", component_property="figure"),
    Input(component_id="color-col", component_property="value"),
    Input(component_id="perplex-slider", component_property="value")
)
def pokemon_tsne(color_column, perplexity_curse):
    """POKEMON TSNE 
    
    Keyword arguments:
    color_column -- change the column to color the plot
    perplexity_curse -- change the perplexity value of the tsne algorithm
    Return: scatter plot  
    """
    tsne= TSNE(perplexity=perplexity_curse)
    score = pd.DataFrame(tsne.fit_transform(final_df),
                         index=final_df.index,
                         columns=tsne.get_feature_names_out())
    
    score = score.merge(raw_df, left_index=True,
                        right_index=True, how="left")
    fig = px.scatter(score,
                     x="tsne0",
                     y="tsne1",
                     color=color_column,
                     hover_name=score.index,
                     hover_data=score.columns)
    return fig