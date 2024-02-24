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

# Initialiser un dictionnaire pour stocker le nombre total de commentaires par plat
dish_counts = {dish: 0 for dish in df_dishes['name']}

# Initialiser un dictionnaire pour stocker la note moyenne de chaque plat
dish_ratings = {dish: 0 for dish in df_dishes['name']}

# Parcourir chaque commentaire
for _, row in df_comments.iterrows():
    stars = row['stars']
    comment = row['text'].lower().split()  # Diviser le commentaire en mots
    comment = [word for word in comment if word not in stop_words]  # Supprimer les stopwords
    # Compter le nombre de fois que chaque plat apparaît dans le commentaire
    for dish in df_dishes['name']:
        if dish in comment:
            dish_counts[dish] += 1
            dish_ratings[dish] += stars

# Calculer la note moyenne de chaque plat
for dish in dish_ratings:
    if dish_counts[dish] != 0:
        dish_ratings[dish] /= dish_counts[dish]

# Trier les plats par nombre d'occurrences
sorted_dish_counts = sorted(dish_counts.items(), key=lambda x: x[1], reverse=True)

# Extraire les noms de plat et les occurrences pour les 20 premiers plats
top_dishes = [dish[0] for dish in sorted_dish_counts[:20]]
top_occurrences = [count[1] for count in sorted_dish_counts[:20]]
top_ratings = [dish_ratings[dish] for dish in top_dishes]

# Affichage de l'histogramme horizontal
plt.figure(figsize=(10, 8))
bars = plt.barh(top_dishes, top_occurrences, color='skyblue')
plt.xlabel('Nombre d\'occurrences')
plt.ylabel('Plats')
plt.title('Nombre d\'occurrences des 20 plats les plus cités dans les commentaires avec leur note moyenne')

# Ajouter les notes au-dessus des barres
for bar, rating in zip(bars, top_ratings):
    plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{rating:.2f}', 
             va='center', ha='left')

plt.gca().invert_yaxis()  # Inverser l'axe y pour afficher le plat le plus cité en haut
plt.tight_layout()  # Ajuster la disposition pour éviter que les étiquettes ne se chevauchent
plt.savefig('top_20_dishes_occurrences_with_ratings.png')  # Enregistrer l'image
plt.show()
