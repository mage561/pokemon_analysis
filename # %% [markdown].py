# %% [markdown]
# # Loading DF 

# %%
#from dash import Dash, html, dcc, Input, Output
#import dash_cytoscape as cyto

import networkx as nx

import numpy as np
import pandas as pd
import yaml
import os

with open(os.path.join('data', 'pokemon-forms.yaml'), 'r') as file:
    data = yaml.safe_load(file)

pokemon_forms = pd.DataFrame(data).T
def to_numeric(df : pd.DataFrame):
    for i in df.columns:
        try : 
            df[i] = pd.to_numeric(df[i])
        except Exception as e: 
            pass
to_numeric(pokemon_forms)

# %% [markdown]
# # Preprocessing 

# %% [markdown]
# ## Unfolding stats

# %%

stats = pd.DataFrame()
for row in pokemon_forms.index:
    new_line = pd.DataFrame(list(pokemon_forms.loc[row, "stats"].values()), 
                        index=pokemon_forms.loc[row, "stats"].keys(), 
                        columns=[row]).T
    stats = pd.concat([stats, new_line])
to_numeric(stats)
pokemon_forms.merge(stats, right_index=True, left_index=True)
pokemon_forms = pokemon_forms.drop(columns=["stats", "release", "pokemonid", 
                                            "formid", "gender", "ev-yield"])


# %% [markdown]
# ## One hot encoder 

# %%
pokemon_forms_0 = pd.get_dummies(pokemon_forms, 
                                columns=['type1', 'type2'], prefix="", 
                                prefix_sep='')
pokemon_forms_0 = pd.get_dummies(pokemon_forms, columns=["species"])

growth_rate = {'medium slow' : 2, 
                'medium fast' : 3, 
                'fast' : 4, 
                'slow' : 1, 
                'fluctuating' : 0,
                'erratic': 5}
pokemon_forms_0["growth-rate"] = pokemon_forms["growth-rate"].map(growth_rate)
pokemon_forms_0 = pokemon_forms_0.drop(columns=["type1", 
                                            "type2", 
                                            "formname",
                                            "growth-rate"])
pokemon_forms_0.head()

# %% [markdown]
# ## DROP NA

# %%
pokemon_forms_0.count()

# %%
pokemon_forms_0.dropna(axis=0, inplace=True)

# %%
pokemon_forms_0.count(0)

# %% [markdown]
# 
# ## Normalizer

# %%
from sklearn.preprocessing import Normalizer

scaler = Normalizer()
numeric_columns = pokemon_forms.select_dtypes(include=[np.number]).columns
pokemon_forms_0[numeric_columns] = scaler.fit_transform(pokemon_forms_0[numeric_columns])

# %%
to_numeric(pokemon_forms_0)

# %% [markdown]
# # TSNE

# %%
from sklearn.manifold import TSNE
for i in [5, 30, 50, 100]:
    tsne = TSNE()
    tsne_score = pd.DataFrame(tsne.fit_transform(pokemon_forms_0), 
                            index=pokemon_forms_0.index, 
                            columns=tsne.get_feature_names_out())
    


# %%
tsne.get_feature_names_out()

# %%
import plotly.express as px
px.scatter(tsne_score, x=tsne_score["tsne0"], y=tsne_score["tsne1"], hover_name=tsne_score.index)

# %%
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
inertias=[]
for i in range(1,10): 
    kmeans = KMeans(n_clusters=i, random_state=0)
    kmeans.fit(tsne_score)
    inertias.append(kmeans.inertia_)

plt.plot(range(1,10), inertias)
plt.xlabel("Number of clusters")
plt.ylabel('Inertia')

# %%
kmeans = KMeans(n_clusters= 7, random_state=0)

kmeans.fit(tsne_score)

predict_cluster_indexes = kmeans.predict(tsne_score)
poke_cluster = tsne_score.merge(pd.DataFrame(predict_cluster_indexes, 
        index=tsne_score.index, columns=["label"]), 
        left_index=True, right_index=True)

# %%
type_cluster = tsne_score.merge(pokemon_forms, left_index=True, right_index=True)

# %%
type_cluster.columns

# %%

px.scatter(type_cluster, 
           x=type_cluster["tsne0"], 
           y=type_cluster["tsne1"], 
           color=type_cluster["weight"],
           color_discrete_sequence= px.colors.qualitative.Dark24,
           hover_name=type_cluster.index,
           hover_data=["type1", "type2", "species", "height", "weight", 
                       "catch-rate", "base-exp", "egg-cycles", "friendship", 
                       "growth-rate" ]
           )


# %%
px.scatter(poke_cluster, x=poke_cluster["tsne_0"], 
           y=poke_cluster["tsne_1"], 
           color=poke_cluster["label"], 
           hover_name=poke_cluster.index,
           color_continuous_scale=px.colors.qualitative.Plotly)

# %% [markdown]
# ## PCA 

# %%
pokemon_forms_0.shape

# %%
from sklearn.decomposition import PCA
evr = 1
_, i = pokemon_forms_0.shape
while evr >0.9:
    
    poke_pca = PCA(n_components=i, random_state=42)
    pca_res = poke_pca.fit_transform(pokemon_forms_0)
    evr = sum(poke_pca.explained_variance_ratio_)
    if i%10 == 0:
        print(i, ":", evr)
    i-=1
#print("variance expliquée: ", poke_pca.explained_variance_ratio_)
#print("somme des variances:", sum(poke_pca.explained_variance_ratio_))
PCA_res = pd.DataFrame(pca_res, index=pokemon_forms_0.index)

# %%
PCA_res.info()

# %%
print("variance expliquée: ", poke_pca.explained_variance_ratio_)
print("somme des variances:", sum(poke_pca.explained_variance_ratio_))

# %%
import plotly.express as px 

px.scatter(PCA_res, x= 0, y=1, color=3, hover_name=PCA_res.index)

# %% [markdown]
# # Clustering ? 

# %%
PCA_res

# %%
kmeans  = KMeans(n_clusters= 5, random_state=0)

kmeans.fit(pokemon_forms_dummies)

predict_cluster_indexes = kmeans.predict(pokemon_forms_dummies)

# %%
poke_cluster = PCA_res.merge(pd.DataFrame(predict_cluster_indexes, 
        index=PCA_res.index, columns=["label"]), 
        left_index=True, right_index=True)

# %%
poke_cluster

# %%
px.scatter(poke_cluster, x=0, y=2, color=poke_cluster["label"], hover_name=poke_cluster.index)

# %%
pokemon_forms["label"] = poke_cluster["label"]


# %%
clus0 = pokemon_forms.loc[pokemon_forms['label'] == 0]
clus1 = pokemon_forms.loc[pokemon_forms['label'] == 1]
clus2 = pokemon_forms.loc[pokemon_forms['label'] == 2]
clus0.describe(include="all")

# %%
pokemon_forms.info()

# %% [markdown]
# t-SNE

# %%
inertias=[]
for i in range(1,50): 
    kmeans = KMeans(n_clusters=i, random_state=0)
    kmeans.fit(poke50)
    inertias.append(kmeans.inertia_)

plt.plot(range(1,50), inertias)
plt.xlabel("Number of clusters")
plt.ylabel('Inertia')

# %%
kmeans  = KMeans(n_clusters= 20, random_state=0)

kmeans.fit(poke50)



predict_cluster_indexes = pd.DataFrame(kmeans.predict(poke50), index=poke50.index)

cluster20 = poke50.merge(pd.DataFrame(predict_cluster_indexes, 
        index=poke50.index, columns=["label"]), 
        left_index=True, right_index=True)


# %%
cluster20.describe()

# %%

px.scatter_3d(cluster20, 
              x=cluster20.columns[0], 
              y=cluster20.columns[1], 
              z= cluster20.columns[2], 
              color=cluster20.columns[3],
              size=(cluster20.columns[4]),
              hover_name=cluster20.index)


# %%
tsne= TSNE()

poke_tsne = pd.DataFrame(tsne.fit_transform(poke50), index=pokemon_forms_dummies.index)


