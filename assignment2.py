import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

df = pd.read_csv('golf_data.csv')
columns_to_keep = ['player', 'sg_putt', 'sg_arg', 'sg_app', 'sg_ott', 'sg_t2g', 'sg_total']
df = df[columns_to_keep]
df = df.dropna()

interesting_features = df.columns.tolist()
interesting_features.remove('player')

pivot_table = df.pivot_table(index='player', values=interesting_features, aggfunc='mean')
similarity_matrix = cosine_similarity(pivot_table)
similarity_df = pd.DataFrame(similarity_matrix, index=pivot_table.index, columns=pivot_table.index)

players = ['Tiger Woods', 'Rickie Fowler', 'Jon Rahm']
for player in players:
    print(f'Top 10 players similar to {player}:')
    print(similarity_df[player].sort_values(ascending=False)[1:11])
    print('\n')
