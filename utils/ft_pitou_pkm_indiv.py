import yaml
import requests
import pandas as pd
import plotly.graph_objects as go
import matplotlib.colors as mcolors

from PIL import Image
from io import BytesIO

# Chargement des données
def ft_load_pokemon_dataset():
    with open("./data/pokemon-forms.yaml", 'r') as file:
        data = yaml.safe_load(file)
    data_list = [value for value in data.values()]
    return pd.DataFrame(data_list)

# Variables
type_link = {
    "normal": "https://archives.bulbagarden.net/media/upload/0/08/NormalIC_SV.png",
    "fighting": "https://archives.bulbagarden.net/media/upload/0/0f/FightingIC_SV.png",
    "flying": "https://archives.bulbagarden.net/media/upload/d/d7/FlyingIC_SV.png",
    "poison": "https://archives.bulbagarden.net/media/upload/9/9d/PoisonIC_SV.png",
    "ground": "https://archives.bulbagarden.net/media/upload/f/f8/GroundIC_SV.png",
    "rock": "https://archives.bulbagarden.net/media/upload/3/32/RockIC_SV.png",
    "bug": "https://archives.bulbagarden.net/media/upload/d/d1/BugIC_SV.png",
    "ghost": "https://archives.bulbagarden.net/media/upload/2/2c/GhostIC_SV.png",
    "steel": "https://archives.bulbagarden.net/media/upload/b/b8/SteelIC_SV.png",
    "fire": "https://archives.bulbagarden.net/media/upload/a/a2/FireIC_SV.png",
    "water": "https://archives.bulbagarden.net/media/upload/d/de/WaterIC_SV.png",
    "grass": "https://archives.bulbagarden.net/media/upload/7/7b/GrassIC_SV.png",
    "electric": "https://archives.bulbagarden.net/media/upload/7/77/ElectricIC_SV.png",
    "psychic": "https://archives.bulbagarden.net/media/upload/1/13/IceIC_SV.png",
    "ice": "https://archives.bulbagarden.net/media/upload/9/96/PsychicIC_SV.png",
    "dragon": "https://archives.bulbagarden.net/media/upload/7/7f/DragonIC_SV.png",
    "dark": "https://archives.bulbagarden.net/media/upload/3/30/DarkIC_SV.png",
    "fairy": "https://archives.bulbagarden.net/media/upload/c/c6/FairyIC_SV.png"
}

stat_names = {
    'hp': 'HP',
    'attack': 'Attack',
    'defense': 'Defense',
    'spatk': 'Sp. Atk.',
    'spdef': 'Sp. Def.',
    'speed': 'Speed'
}

stat_colormap = mcolors.LinearSegmentedColormap.from_list("pokemon_stat", ["red", "yellow", "lime"], N=160)

def get_pokemon_image(pokemon_id):
    url = f"https://img.pokemondb.net/artwork/large/{pokemon_id}.jpg"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error downloading image: {e}")

def ft_pkm_radar_plot(pokemon):
    fig = go.Figure()
    
    max_stat = max(pokemon['stats'].values())
    radius_max = max(130, max_stat)
    
    # Ajout du radar
    fig.add_trace(go.Scatterpolar(
        r=list(pokemon['stats'].values()),
        theta=list(pokemon['stats'].keys()),
        fill='toself',
        name=pokemon['pokemonid'],
        opacity=0.5
    ))
    
    fig.update_layout(
        polar=dict(domain=dict(x=[0.65, 0.95], y=[0, 1]),
        radialaxis=dict(range=[0, radius_max]
        )
))
    return fig

def ft_pkm_bar_plot(pokemon):
    fig = go.Figure()
    
    max_stat = max(pokemon['stats'].values())
    x_max = max(135, max_stat)
    
    # Ajout des barres
    for stat, value in pokemon['stats'].items():
        fig.add_trace(go.Bar(
            y=[f"{stat_names[stat]} "],
            x=[value],
            text=[f"{value}"],
            orientation='h',
            marker_color=mcolors.to_hex(stat_colormap(value)),
            showlegend=False,
            opacity=0.7
        ))
        
    fig.update_layout(
        xaxis=dict(domain=[0.65, 0.95], range=[0, x_max]),
        yaxis=dict(domain=[0.2, 0.8])
    )
    return fig

def ft_add_pokemon_images(fig, pokemon, plot_type):    
    # Ajout de l'image du Pokémon
    fig.add_layout_image(
        dict(
            source=Image.open(BytesIO(get_pokemon_image(pokemon['pokemonid']))),
            x=0.15, y=0.5, 
            sizex=0.3, 
            sizey=1,
            xanchor='center', 
            yanchor='middle'
        )
    )
    
    # Ajout du titre
    fig.update_layout(
        title=dict(
            text=f"{pokemon['pokemonid'].upper()}",
            x=0.45, y=0.6,
            xanchor='center',
            yanchor='middle',
            font=dict(
                size=36,
                family="Courier New",
                color='Black'
            )
        )
    )
    
    # Ajout des types
    fig.add_layout_image(
        dict(
            source=Image.open(BytesIO(requests.get(type_link[pokemon['type1']]).content)),
            x=0.45, y=0.5,
            sizex=0.15, sizey=1,
            xanchor='center', yanchor='middle'
        )
    )
    
    if pokemon['type2'] is not None:
        fig.add_layout_image(
            dict(
                source=Image.open(BytesIO(requests.get(type_link[pokemon['type2']]).content)),
                x=0.45, y=0.3,
                sizex=0.15, sizey=1,
                xanchor='center', yanchor='middle'
            )
        )
    return fig