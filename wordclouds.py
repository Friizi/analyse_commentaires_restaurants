import spacy
import csv
from collections import defaultdict, Counter
from datetime import datetime
from wordcloud import WordCloud
import os

# Charger le modèle de langue anglaise de SpaCy
nlp = spacy.load("en_core_web_sm")

# Fonction pour extraire les entités d'un commentaire
def extract_entities(comment):
    doc = nlp(comment)
    entities = [ent.text for ent in doc.ents]
    # Filtrer pour conserver uniquement les entités de type 'PRODUCT'
    # entities = [ent.text for ent in doc.ents if ent.label_ == 'PRODUCT']
    return entities

# Fonction pour déterminer si un commentaire est positif ou négatif
def determine_sentiment(stars):
    if stars > 2:
        return "positive"
    elif stars <= 2:
        return "negative"
    else:
        return "neutral"

# Chemin vers votre fichier CSV contenant les commentaires
csv_file_path = "query_result1.csv"

# Dossier pour stocker les nuages de mots par mois
output_folder = "wordclouds"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Initialisation d'un dictionnaire pour stocker les entités par mois et sentiment
entities_by_month = defaultdict(lambda: {'positive': Counter(), 'negative': Counter()})

# Ouvrir le fichier CSV et lire les données
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Extraire la date et la note du commentaire depuis les colonnes appropriées du CSV
        comment_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
        month_year = comment_date.strftime('%Y-%m')
        stars = int(row['stars'])
        
        # Extraire le texte du commentaire depuis la colonne appropriée du CSV
        comment_text = row['text']
        
        # Extraire les entités du commentaire
        entities = extract_entities(comment_text)
        
        # Accumuler les entités dans le dictionnaire par mois et sentiment
        sentiment = determine_sentiment(stars)
        entities_by_month[month_year][sentiment].update(entities)

# Génération et enregistrement des nuages de mots pour chaque mois et sentiment
for month_year, sentiments in entities_by_month.items():
    # Créer un dossier pour le mois s'il n'existe pas déjà
    month_folder = os.path.join(output_folder, month_year)
    if not os.path.exists(month_folder):
        os.makedirs(month_folder)
    
    for sentiment, entity_counts in sentiments.items():
        # Générez le nuage de mots ici si des entités existent
        if entity_counts:
            wordcloud_text = ' '.join([entity for entity, count in entity_counts.items() for _ in range(count)])
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(wordcloud_text)
            
            # Enregistrez le nuage de mots dans le dossier du mois
            wordcloud.to_file(os.path.join(month_folder, f"wordcloud_{sentiment}.png"))
