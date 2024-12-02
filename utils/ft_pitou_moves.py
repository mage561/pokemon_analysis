import yaml
import pandas as pd
import plotly.express as px
from sklearn.manifold import TSNE

def ft_load_moves_dataset():
    # Chargement des données des moves
    with open('./data/moves.yaml', 'r') as file:
        moves_data = yaml.safe_load(file)
    data_list = [value for value in moves_data.values()]
    moves_df = pd.DataFrame(data_list)
    
    # Nettoyage des données
    moves_df['power'] = pd.to_numeric(moves_df['power'], errors='coerce').fillna(0)
    moves_df['accuracy'] = pd.to_numeric(moves_df['accuracy'], errors='coerce').fillna(100)
    moves_df['pp'] = pd.to_numeric(moves_df['pp'], errors='coerce').fillna(10)
    
    return moves_df

def ft_moves_dual_acps(moves_df):
    fig = px.scatter_matrix(
        moves_df,
        dimensions=["power", "accuracy", "pp", "priority"],
        color='name'
    )
    fig.update_traces(diagonal_visible=False)
    return fig

def ft_moves_tsne(moves_df):
    # Sélection des variables
    features = moves_df[["power", "accuracy", "pp", "priority"]]
    
    # Calcul t-SNE
    tsne = TSNE(n_components=2, random_state=0)
    projections = tsne.fit_transform(features)
    
    # Ajout des projections au DataFrame
    moves_df = moves_df.copy()
    moves_df['x'] = projections[:, 0]
    moves_df['y'] = projections[:, 1]
    
    fig = px.scatter(
        moves_df,
        x='x', 
        y='y',
        color='category', 
        hover_name='name',
        hover_data=['type', 'power', 'accuracy', 'pp', 'category'],
        labels={'x': 't-SNE 1', 'y': 't-SNE 2'}
    )
    return fig