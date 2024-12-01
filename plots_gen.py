
import plotly.express as px
import numpy as np
import pandas as pd

from load_dataset import pokemon_dataset, to_numeric, preprocessed_dataset
from sklearn.manifold import TSNE
final_df = preprocessed_dataset()
raw_df = pokemon_dataset()
"""
This file contains all the functions for the plots 
"""


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

def scatter_everything(x,y, color, symbol):
    fig = px.scatter(raw_df,
                     x=x,
                     y=y,
                     color=color,
                     symbol=symbol,
                     hover_name=raw_df.index,
                     hover_data=raw_df.columns)
    return fig