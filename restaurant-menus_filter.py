import pandas as pd
import re

# Charger le fichier CSV original
df = pd.read_csv('restaurant-menus_filtered.csv')

# Filtrer les lignes où la colonne 'name' a plus de 50 caractères
# df_filtered = df[df['name'].str.len() <= 50]

# Retirer les retours à la ligne (\n) à la fin de chaque nom de plat
# df_filtered['name'] = df_filtered['name'].str.replace(r'\s*$', '', regex=True)

# Retirer les caractères spéciaux et les nombres de la colonne 'name'
# df_filtered['name'] = df_filtered['name'].apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', x))

# Supprimer les doubles espaces ou plus dans la colonne 'name'
df['name'] = df['name'].apply(lambda x: re.sub(r'\s{2,}', ' ', x))

# Retirer les espaces en fin de chaque ligne dans la colonne 'name'
df['name'] = df['name'].str.rstrip()

# Supprimer les doublons dans la colonne 'name'
df = df.drop_duplicates(subset=['name'], keep='first')

# Conserver uniquement la colonne 'name'
df_filtered = df[['name']]

# Enregistrer le nouveau fichier CSV
df_filtered.to_csv('restaurant-menus_filtered1.csv', index=False)
