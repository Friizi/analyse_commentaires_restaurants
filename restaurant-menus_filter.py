import pandas as pd
import re

# Charger le fichier CSV original
df = pd.read_csv('restaurant-menus.csv')

# Filtrer les lignes où la colonne 'name' a plus de 50 caractères
df_filtered = df[df['name'].str.len() <= 50]

# Retirer les retours à la ligne (\n) à la fin de chaque nom de plat
df_filtered['name'] = df_filtered['name'].str.replace(r'\s*$', '', regex=True)

# Retirer les caractères spéciaux et les nombres de la colonne 'name'
df_filtered['name'] = df_filtered['name'].apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', x))

# Supprimer les doublons dans la colonne 'name'
df_filtered = df_filtered.drop_duplicates(subset=['name'], keep='first')

# Conserver uniquement la colonne 'name'
df_filtered = df_filtered[['name']]

# Enregistrer le nouveau fichier CSV
df_filtered.to_csv('restaurant-menus_filtered.csv', index=False)
