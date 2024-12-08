import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

# Création des cartes pour chaque rubrique
cards = [
    {
        "title": "Histogramme",
        "image": "/assets/img/histogram.png",
        "path": "/histogram"
    },
    {
        "title": "Mouvements",
        "image": "/assets/img/moves.png",
        "path": "/moves"
    },
    {
        "title": "Vue Globale",
        "image": "/assets/img/pkm_global.png",
        "path": "/pkm_global"
    },
    {
        "title": "Vue Individuelle",
        "image": "/assets/img/pkm_indiv.png",
        "path": "/pkm_indiv"
    },
    {
        "title": "Types",
        "image": "/assets/img/types.png",
        "path": "/types"
    }
]

# Création du layout
layout = html.Div([
    # En-tête
    html.Div([
        html.H1('Dashboard Pokémon', className='h3 mb-4 text-gray-800'),
        html.P('Sélectionnez une rubrique pour explorer les données', className='mb-4')
    ], className='container-fluid'),

    # Grille de cartes
    html.Div([
        html.Div([
            # Création des cartes
            html.Div([
                dcc.Link([
                    html.Div([
                        # Carte
                        html.Div([
                            # Contenu de la carte
                            html.Div([
                                html.H5(card["title"], className='card-title')
                            ], className='card-body'),
                            # Image
                            html.Div([
                                html.Img(src=card["image"], className='img-fluid')
                            ], className='card-img-top col-11 my-3 ')
                        ], className='card shadow my-3 col-12 align-items-center', style={'background': 'rgba(0, 0, 0, 0.05)'})
                    ], className='col-12')
                ], href=card["path"])
                for card in cards
            ], className='row')
        ], className='container-fluid')
    ])
], className='container-fluid')