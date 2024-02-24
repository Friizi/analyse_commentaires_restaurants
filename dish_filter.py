import pandas as pd

# Charger le fichier CSV original
df = pd.read_csv('Dish.csv')

# Filtrer les lignes où la colonne 'name' a plus de 50 caractères
df_filtered = df[df['name'].str.len() <= 50]

# Conserver uniquement la colonne 'name'
df_filtered = df_filtered[['name']]

# Enregistrer le nouveau fichier CSV
df_filtered.to_csv('Dish_filtered.csv', index=False)
