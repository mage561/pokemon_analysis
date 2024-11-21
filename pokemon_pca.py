

from dash import Dash, html, dcc, Input, Output
import dash_cytoscape as cyto
import numpy as np
import networkx as nx


import pandas as pd
import yaml
import os

with open(os.path.join('data', 'pokemon-forms.yaml'), 'r') as file:
    data = yaml.safe_load(file)

pokemon_forms = pd.DataFrame(data).T

for row in pokemon_forms.index:
    stats = pd.DataFrame(pokemon_forms.loc[row, "stats"], index=pokemon_forms.index)

pokemon_forms = pd.merge(pokemon_forms, stats, left_index=True, right_index=True)
pokemon_forms = pokemon_forms.drop("stats", axis = 1)

pokemon_forms["gen"] = pokemon_forms["gen"].astype("int64")
num = ["height", "weight", "catch-rate", "base-exp", "egg-cycles", "friendship" ]
for col in num : 
    pokemon_forms[col] = pokemon_forms[col].replace('None', np.NaN)
    #pokemon_forms[col] = pokemon_forms[col].astype("int64")
    print(f"{col} has {pokemon_forms[col].isna().sum()} None values")
    pokemon_forms[col].fillna(np.nan)
    pokemon_forms[col] = pd.to_numeric(pokemon_forms[col])



