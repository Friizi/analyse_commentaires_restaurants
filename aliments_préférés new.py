from rapidfuzz import process, fuzz
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Télécharger les ressources de NLTK
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Initialiser le lemmatiseur et les stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Fonction pour pré-traiter et normaliser les noms des plats
def preprocess_dish_name(name):
    name = name.lower().strip()
    # Tokeniser le nom du plat
    tokens = word_tokenize(name)
    # Lemmatiser chaque mot (les convertir en singulier)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    # Rejoindre les tokens en une chaîne de caractères
    normalized_name = ' '.join(lemmatized_tokens)
    return normalized_name

# Charger les données des commentaires et des plats
df_comments = pd.read_csv('query_result7.csv')
df_dishes = pd.read_csv('restaurant-menus_filtered.csv')

# Prétraiter les noms des plats
df_dishes['name'] = df_dishes['name'].apply(preprocess_dish_name)
dish_names = df_dishes['name'].dropna().unique().tolist()

# Fonction pour trouver les correspondances floues
def find_fuzzy_matches(comment, choices, score_cutoff=86):
    # Utilisation de la fonction extract pour obtenir toutes les correspondances au-dessus du seuil
    matches = process.extract(comment, choices, scorer=fuzz.WRatio, score_cutoff=score_cutoff, limit=None)
    return [match[0] for match in matches]

# Compter les occurrences et les notes des plats
dish_counts = {}
dish_ratings = {}

# Parcourir chaque commentaire
for _, row in df_comments.iterrows():
    stars = row['stars']
    comment = row['text'].lower()
    # Tokeniser et lemmatiser le commentaire
    comment_tokens = word_tokenize(comment)
    lemmatized_comment_tokens = [lemmatizer.lemmatize(token) for token in comment_tokens]
    # Supprimer les stopwords
    filtered_comment_tokens = [token for token in lemmatized_comment_tokens if token not in stop_words]
    comment = ' '.join(filtered_comment_tokens)
    # Trouver les correspondances
    matches = find_fuzzy_matches(comment, dish_names)
    for match in matches:
        normalized_dish = preprocess_dish_name(match)
        dish_counts[normalized_dish] = dish_counts.get(normalized_dish, 0) + 1
        dish_ratings[normalized_dish] = dish_ratings.get(normalized_dish, 0) + stars

# Calculer la note moyenne pour chaque plat mentionné
for dish in dish_ratings:
    if dish_counts[dish]:
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
plt.savefig('top_20_dishes_occurrences_with_ratings_7.png')
plt.show()