from rapidfuzz import process, fuzz
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

# Télécharger les stopwords de NLTK (seulement la première fois)
nltk.download('stopwords')

# Charger les données des commentaires
df_comments = pd.read_csv('query_result1.csv')

# Charger les données des plats
df_dishes = pd.read_csv('restaurant-menus_filtered.csv')

# Initialiser les stopwords
stop_words = set(stopwords.words('english'))

# Fonction pour pré-traiter et normaliser les noms des plats
def preprocess_dish_name(name):
    name = name.lower().strip()
    # Ajouter d'autres règles de prétraitement au besoin
    return name

# Prétraiter les noms des plats
df_dishes['name'] = df_dishes['name'].apply(preprocess_dish_name)
dish_names = df_dishes['name'].dropna().unique().tolist()

# Fonction pour trouver les correspondances floues
def find_fuzzy_matches(comment, choices, score_cutoff=86):
    matches = process.extract(comment, choices, scorer=fuzz.WRatio, score_cutoff=score_cutoff, limit=None)
    return [match[0] for match in matches]

# Compter les occurrences et les notes des plats
dish_counts = {}
dish_ratings = {}

# Parcourir chaque commentaire
for _, row in df_comments.iterrows():
    stars = row['stars']
    comment = ' '.join([word for word in row['text'].lower().split() if word not in stop_words])
    matches = find_fuzzy_matches(comment, dish_names)
    for match in matches:
        normalized_dish = preprocess_dish_name(match)
        dish_counts[normalized_dish] = dish_counts.get(normalized_dish, 0) + 1
        dish_ratings[normalized_dish] = dish_ratings.get(normalized_dish, 0) + stars

# Calculer la note moyenne pour chaque plat mentionné
for dish in dish_ratings:
    dish_ratings[dish] /= dish_counts[dish]

# Trier les plats par nombre d'occurrences et obtenir les 20 premiers
sorted_dish_counts = sorted(dish_counts.items(), key=lambda x: x[1], reverse=True)[:20]
top_dishes, top_occurrences = zip(*sorted_dish_counts)
top_ratings = [dish_ratings[dish] for dish in top_dishes]

# Générer l'histogramme
plt.figure(figsize=(10, 8))
bars = plt.barh(top_dishes, top_occurrences, color='skyblue')
plt.xlabel('Nombre d\'occurrences')
plt.ylabel('Plats')
plt.title('Top 20 des plats les plus cités dans les commentaires avec leur note moyenne')

for bar, rating in zip(bars, top_ratings):
    plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{rating:.2f}', va='center', ha='left')

plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('top_20_dishes_occurrences_with_ratings.png')
plt.show()
