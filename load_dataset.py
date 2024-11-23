import pandas as pd
import numpy as np
import os
import yaml
from sklearn.preprocessing import Normalizer
def to_numeric(df : pd.DataFrame):
    for i in df.columns:
        try : 
            df[i] = pd.to_numeric(df[i])
        except Exception as e: 
            pass

def pokemon_dataset():
    "load pokemon forms dataset"
    with open(os.path.join('data', 'pokemon-forms.yaml'), 'r') as file:
        data = yaml.safe_load(file)

    pokemon_forms = pd.DataFrame(data).T
    stats = pd.DataFrame()
    for row in pokemon_forms.index:
        new_line = pd.DataFrame(list(pokemon_forms.loc[row, "stats"].values()), 
                            index=pokemon_forms.loc[row, "stats"].keys(), 
                            columns=[row]).T
        stats = pd.concat([stats, new_line])
        pokemon_forms.merge(stats, right_index=True, left_index=True)
        to_numeric(pokemon_forms)
        return pokemon_forms
    

growth_rate = {'medium slow' : 2, 
                'medium fast' : 3, 
                'fast' : 4, 
                'slow' : 1, 
                'fluctuating' : 0,
                'erratic': 5}


def preprocessed_dataset():
    """pokemon preprocessing
    
    
    Return: OHC and Normalised dataset, no NaN
    """
    pokemon = pokemon_dataset()
    pokemon = pokemon.drop(columns=["stats",
                                    "release", 
                                    "pokemonid",
                                    "formid",
                                    "gender", 
                                    "ev-yield"])


    # One hot encoder
    pokemon_0 = pd.get_dummies(pokemon,
                                columns=['type1', 'type2'], 
                                prefix="",
                                prefix_sep='')
    pokemon_0 = pd.get_dummies(pokemon,
                               columns=["species", "growth-rate"])
    
    #pokemon_0["growth-rate"] = pokemon["growth-rate"].map(growth_rate)
    pokemon_0 = pokemon_0.drop(columns=["type1",
                                        "type2", 
                                        "formname",
                                        
                                        ])

    pokemon_0.dropna(axis=0, inplace=True)

    scaler = Normalizer()
    num_cols = pokemon.select_dtypes(include=[np.number]).columns
    pokemon_0[num_cols] = scaler.fit_transform(pokemon_0[num_cols])
    
    to_numeric(pokemon_0)

    return pokemon_0
