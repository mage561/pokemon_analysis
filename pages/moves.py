import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
from utils.ft_pitou_moves import ft_load_moves_dataset, ft_moves_dual_acps, ft_moves_tsne

# Enregistrement de la page
dash.register_page(__name__, path='/moves')

# Layout de la page avec le style SB Admin 2
layout = html.Div([
    # Page Heading
    html.Div([
        html.H1("Analyse des Moves Pokémon", className="h3 mb-0 text-gray-800")
    ], className="d-sm-flex align-items-center justify-content-between mb-4"),

    # Content Row
    html.Div([
        # Scatter Matrix Card
        html.Div([
            html.Div([
                # Card Header
                html.Div([
                    html.H6("Matrice de Dispersion", className="m-0 font-weight-bold text-primary")
                ], className="card-header py-3"),
                # Card Body
                html.Div([
                    dcc.Graph(
                        id='scatter-matrix',
                        className='chart-area'
                    )
                ], className="card-body")
            ], className="card shadow mb-4")
        ], className="col-xl-6 col-lg-6"),

        # t-SNE Plot Card
        html.Div([
            html.Div([
                # Card Header
                html.Div([
                    html.H6("Analyse t-SNE", className="m-0 font-weight-bold text-primary")
                ], className="card-header py-3"),
                # Card Body
                html.Div([
                    dcc.Graph(
                        id='tsne-plot',
                        className='chart-area'
                    )
                ], className="card-body")
            ], className="card shadow mb-4")
        ], className="col-xl-6 col-lg-6")
    ], className="row")
], className="container-fluid")

@callback(
    [Output('scatter-matrix', 'figure'),
     Output('tsne-plot', 'figure')],
    Input('scatter-matrix', 'id')
)
def update_graphs(_):
    moves_df = ft_load_moves_dataset()
    scatter_matrix = ft_moves_dual_acps(moves_df)
    tsne_plot = ft_moves_tsne(moves_df)
    return scatter_matrix, tsne_plot