import pandas as pd
import numpy as np
import os
import yaml
from sklearn.preprocessing import Normalizer

def load_file():
    with open(os.path.join('data', 'pokemon-forms.yaml'), 'r') as file:
        data = yaml.safe_load(file)
    pokemon_forms = pd.DataFrame(data).T

    return pokemon_forms

def to_numeric(df : pd.DataFrame):
    for i in df.columns:
        try : 
            df[i] = pd.to_numeric(df[i])
        except Exception as e: 
            pass

def poke_stats() -> pd.DataFrame:
    """Extract and return the stats of each Pokémon form as a DataFrame."""
    pokemon_forms = load_file()
    stats = pd.DataFrame()
    for row in pokemon_forms.index:
        new_line = pd.DataFrame(pokemon_forms.loc[row, "stats"], index=[row])
        stats = pd.concat([stats, new_line], axis=0)
    return stats

def pokemon_dataset():
    "load pokemon forms dataset"
    pokemon_forms = load_file()
    stats = poke_stats()
    df = pokemon_forms.merge(stats, left_index=True, right_index=True)
    df1 = df.drop(columns=["stats"])
    to_numeric(df1)
    return df1
    
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
    pokemon = pokemon.drop(columns=[
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
    #pokemon_0 = pd.get_dummies(pokemon,
    #                           columns=["species", "growth-rate"])
    
    #pokemon_0["growth-rate"] = pokemon["growth-rate"].map(growth_rate)
    pokemon_0 = pokemon_0.drop(columns=[
                                        "formname",
                                        "species",
                                        "growth-rate"
                                        ])

    pokemon_0.dropna(axis=0, inplace=True)

    scaler = Normalizer()
    num_cols = pokemon.select_dtypes(include=[np.number]).columns
    pokemon_0[num_cols] = scaler.fit_transform(pokemon_0[num_cols])
    
    to_numeric(pokemon_0)

    return pokemon_0


if __name__ == "__main__":
    df = pokemon_dataset()
    print(df.info())