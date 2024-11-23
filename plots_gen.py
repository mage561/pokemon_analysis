
import plotly.express as px
import numpy as np
import pandas as pd

from load_dataset import pokemon_dataset, to_numeric, preprocessed_dataset
from sklearn.manifold import TSNE
final_df = preprocessed_dataset()

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
    
    score = score.merge(pokemon_dataset(), left_index=True,
                        right_index=True, how="left")
    fig = px.scatter(score,
                     x="tsne0",
                     y="tsne1",
                     color=color_column,
                     hover_name=score.index,
                     hover_data=score.columns)
    return fig

def hist_by_type(types, values_x, values_y):
    """HIST BY TYPE
    
    Keyword arguments:
    TYPES -- Types to display
    values_x -- x-axis values
    values_y -- y-axis values
    Return: histogram
    """
    
    fig = px.histogram(x=values_x,
                       y=values_y,
                       color=types)
    return fig