import pandas as pd
import matplotlib.pyplot as plt
import re
from multiprocessing import Pool

# Charger les données des commentaires
df_comments = pd.read_csv('query_result1.csv')

# Charger les données des plats
df_dishes = pd.read_csv('restaurant-menus_filtered.csv')

# Créer une expression régulière pour rechercher les noms de plats
dish_regex = r'\b(?:' + '|'.join(re.escape(name) for name in df_dishes['name']) + r')\b'

# Fonction pour traiter un commentaire
def process_comment(row):
    stars = row['stars']
    comment = row['text']
    # Filtrer les commentaires contenant les noms de plats
    matches = df_dishes[df_dishes['name'].str.contains(dish_regex, case=False)]
    # Extraire les noms de plats de ces commentaires
    matched_dishes = matches['name'].tolist()
    return stars, matched_dishes

# Point d'entrée principal
if __name__ == '__main__':
    # Diviser les commentaires en sous-ensembles
    num_processes = 4
    chunk_size = len(df_comments) // num_processes
    chunks = [df_comments[i:i+chunk_size] for i in range(0, len(df_comments), chunk_size)]

    # Exécuter le traitement en parallèle
    with Pool(num_processes) as pool:
        results = pool.map(process_comment, chunks)

    # Initialiser un dictionnaire pour stocker le nombre total de commentaires par plat
    dish_counts = {dish: 0 for dish in df_dishes['name']}

    # Initialiser un dictionnaire pour stocker la note moyenne de chaque plat
    dish_ratings = {dish: {'total_stars': 0, 'count': 0} for dish in df_dishes['name']}

    # Mettre à jour les comptes de plats pour chaque nom de plat trouvé
    for result in results:
        for stars, matched_dishes in result:
            for dish in matched_dishes:
                dish_counts[dish] += 1
                dish_ratings[dish]['total_stars'] += stars
                dish_ratings[dish]['count'] += 1

    # Calculer la note moyenne de chaque plat
    for dish in dish_ratings:
        if dish_ratings[dish]['count'] != 0:
            dish_ratings[dish]['average_rating'] = dish_ratings[dish]['total_stars'] / dish_ratings[dish]['count']

    # Trier les plats par nombre d'occurrences
    sorted_dish_counts = sorted(dish_counts.items(), key=lambda x: x[1], reverse=True)

    # Extraire les noms de plat et les occurrences pour les 20 premiers plats
    top_dishes = [dish[0] for dish in sorted_dish_counts[:20]]
    top_occurrences = [count[1] for count in sorted_dish_counts[:20]]
    top_ratings = [dish_ratings[dish]['average_rating'] for dish in top_dishes]

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
