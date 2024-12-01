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

app = Dash()
app.layout=html.Div(children=[
    # TSNE
    html.H1("Pokemon TSNE"),
    html.Hr(),
    dcc.Dropdown(options =raw_df.columns, 
                    value="type1", 
                    id="color-col"),
    dcc.Slider(5, 50,  step = 5, 
               value = 30,
               id="perplex-slider"),
    dcc.Graph(figure={}, id="tsne-graph"),

    ## Histogram
    html.H1(" Histogram by type "),
    html.Hr(),
    dcc.Checklist(raw_df["type1"].unique(),
                 value=["Normal"],
                 id="hist-types"),
    dcc.Dropdown(raw_df.columns,
                  value="hp",
                  id="hist-x"),
    dcc.Graph(figure={}, id="hist-by-type"),


    ## SCATTER EVERYTHING
    html.H1("Scatterplot of almost everything"),
    html.Hr(),
    html.H2("x - values"),
    dcc.Dropdown(raw_df.select_dtypes(include =np.number).columns,
                 value="hp",
                 id="scatter-x"),
    html.H2("y-values"),
    dcc.Dropdown(raw_df.select_dtypes(include =np.number).columns,
                 value="hp",
                 id="scatter-y"),
    html.H2("color value"),
    dcc.Dropdown(raw_df.select_dtypes(include ="object").columns,
                 value="type2",
                 id="scatter-color"),
    html.H2("symbol value"),
    dcc.Dropdown(raw_df.select_dtypes(include ="object").columns,
                 value="type1",
                 id="scatter-symb"),
    html.H2("scatterplot"),
    dcc.Graph(figure={}, id="scatter-plot")

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

# scatter plot

@callback(
    Output("scatter-plot", "figure"),
    Input("scatter-x", "value"),
    Input("scatter-y", "value"),
    Input("scatter-color", "value"),
    Input("scatter-symb", "value")
)
def scatter_everything(x,y, color, symbol):
    fig = px.scatter(raw_df,
                     x=x,
                     y=y,
                     color=color,
                     symbol=symbol,
                     hover_name=raw_df.index,
                     hover_data=raw_df.columns)
    return fig

if __name__ == '__main__':
    app.run(debug=True)