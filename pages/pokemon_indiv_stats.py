# pages/pokemon_indiv_stats.py
import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from utils.ft_pitou_pkm_indiv import (
    ft_load_pokemon_dataset, 
    ft_pkm_radar_plot,
    ft_pkm_bar_plot, 
    ft_add_pokemon_images
)

df = ft_load_pokemon_dataset()

# Layout de la page
dash.register_page(__name__, path='/pkm_indiv')

layout = html.Div([
    html.H1("Statistiques individuelles", className="h3 mb-4 text-gray-800"),
    
    html.Div([
        # Barre de recherche
        dcc.Dropdown(
            id='pokemon-search',
            options=[{'label': pokemon.capitalize(), 'value': pokemon} 
                    for pokemon in df['pokemonid'].unique()],
            placeholder="Rechercher un Pokémon...",
            className="mb-4"
        ),
        
        # Sélecteur de graphique
        dcc.RadioItems(
            id='plot-type',
            options=[
                {'label': 'Radar-plot', 'value': 'radar'},
                {'label': 'Barplot', 'value': 'bar'}
            ],
            value='radar',
            className="mb-4"
        ),
        
        # Zone du graphique
        dcc.Graph(id='pokemon-stats-graph')
    ], className="card shadow mb-4")
])

@callback(
    Output('pokemon-stats-graph', 'figure'),
    [Input('pokemon-search', 'value'),
     Input('plot-type', 'value')]
)
def update_graph(selected_pokemon, plot_type):
    if not selected_pokemon:
        return go.Figure()
    
    pokemon = df[df['pokemonid'] == selected_pokemon].iloc[0]
    
    # Création du graphique selon le type sélectionné
    if plot_type == 'radar':
        fig = ft_pkm_radar_plot(pokemon)
    else:
        fig = ft_pkm_bar_plot(pokemon)
    
    # Ajout des images
    fig = ft_add_pokemon_images(fig, pokemon, plot_type)
    
    return fig