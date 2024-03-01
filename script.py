import pandas as pd
from gensim.models import LdaModel
from gensim.corpora.dictionary import Dictionary
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import os
import matplotlib.pyplot as plt

# Chargement des données
df = pd.read_csv('query_result6.csv', parse_dates=['date'])

def preprocess(text):
    # Ajout des stopwords personnalisés, y compris les déterminants et les chiffres en lettres
    custom_stopwords = [
        "the", "a", "an", "this", "that", "these", "those", "my", "your", 
        "his", "her", "its", "our", "their", "some", "any", "no", "every", 
        "each", "all", "both", "either", "neither", "much", "many", "few", 
        "less", "more","one", "two", "three", "four", "five", "six", "seven",
        "eight", "nine", "ten","eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen", "twenty","thirty", "forty", 
        "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand"
    ]
    stop_words = set(stopwords.words('english')).union(custom_stopwords)
    text = re.sub(r'\W', ' ', str(text)).lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

df['processed_text'] = df['text'].apply(preprocess)
df['month_year'] = df['date'].dt.to_period('M')
grouped = df.groupby('month_year')

output_dir = "LDA_results"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for name, group in grouped:
    texts = group['processed_text'].tolist()
    dictionary = Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, passes=10)

    # Extraction des termes dominants pour chaque topic
    topic_terms = {}
    for i in range(lda.num_topics):
        words = lda.show_topic(i, topn=3)
        topic_terms[i] = ', '.join([word for word, prob in words])

    # Écriture des résultats dans un fichier texte
    file_name = f"{name}_LDA_results.txt"
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, 'w') as file:
        file.write(f'Mois : {name}\n')
        file.write('----------------\n')
        for idx, topic in lda.print_topics(-1):
            file.write(f'Topic: {idx} \nWords: {topic}\n')
        file.write('\n\n')

    # Préparation des données pour le graphique
    topic_weights = []
    for i, row_list in enumerate(lda[corpus]):
        row = sorted(row_list, key=lambda x: (x[1]), reverse=True)
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # Le topic dominant
                topic_weights.append((topic_num, prop_topic))

    df_topics = pd.DataFrame(topic_weights, columns=['topic_id', 'weight'])

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10,6))
    topic_counts = df_topics['topic_id'].value_counts().sort_index()
    labels = [topic_terms[i] for i in topic_counts.index]  # Utilisation des termes dominants pour les étiquettes
    ax.bar(labels, topic_counts.values)
    ax.set_xlabel('Topics')
    ax.set_ylabel('Nombre d’occurrences')
    ax.set_title(f'Distribution des topics pour {name}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{name}_topic_distribution.png"))
    plt.close()
