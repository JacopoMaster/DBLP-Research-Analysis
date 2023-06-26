import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

import nltk
from nltk.corpus import stopwords


def create_graph_from_df(G, df):
    for _, row in df.iterrows():
        title = row['title']
        year = row['year']
        G.add_node(title, bipartite=0, year=year)  # aggiungi il nodo della pubblicazione con l'attributo 'year'
        for author in row['author']:
            G.add_node(author, bipartite=1)  # aggiungi il nodo dell'autore
            G.add_edge(title, author)  # aggiungi l'arco tra l'autore e la pubblicazione
    return G


#funzione utile quando 'year' è un oggetto del tipo '2020|2020'
def check_year(year_string):
    if '|' in year_string:
        year1, year2 = year_string.split('|')
        if year1 == year2:
            return int(year1)  # converte in un intero
        else:
            return None  # restituisce None se le date non coincidono
    else:
        return int(year_string)  # se è un singolo anno, converte direttamente in intero



################### Esercizio 1 ###################

def find_publication_with_most_authors(G, year):
    publications = [n for n, d in G.nodes(data=True) if d['bipartite'] == 0 and d['year'] <= year]
    
    max_authors = 0
    max_publication = None
    for publication in publications:
        num_authors = G.degree(publication)
        if num_authors > max_authors:
            max_authors = num_authors
            max_publication = publication

    return max_publication, max_authors



################### Esercizio 2 ###################

english_stopwords = set(stopwords.words('english'))
italian_stopwords = set(stopwords.words('italian'))
french_stopwords = set(stopwords.words('french'))
german_stopwords = set(stopwords.words('german'))
stop_words = english_stopwords.union(italian_stopwords, french_stopwords, german_stopwords)

def find_most_common_word(G, year):
    components = list(nx.connected_components(G))

    common_words = []
    
    for component in components:
        publications = [node for node in component if G.nodes[node]['bipartite'] == 0 and G.nodes[node]['year'] <= year]
        
        if len(publications) >= 30:
            titles = ' '.join(publications)
            words = nltk.word_tokenize(titles.lower())
            words = [word for word in words if word.isalpha() and word not in stop_words]
            common_word = Counter(words).most_common(1)
            common_words.append(common_word)
            
    return common_words



################### Esercizio 3 ###################

def find_publication_with_most_popular_authors(G, year):
    author_popularity = {n: G.degree(n) for n, d in G.nodes(data=True) if d['bipartite'] == 1}

    publications = [n for n, d in G.nodes(data=True) if d['bipartite'] == 0 and d['year'] <= year]

    max_popularity_score = 0
    max_popularity_publication = None
    for publication in publications:
        popularity_score = sum(author_popularity.get(author, 0) for author in G.neighbors(publication))
        if popularity_score > max_popularity_score:
            max_popularity_score = popularity_score
            max_popularity_publication = publication

    return max_popularity_publication, max_popularity_score



# Funzione che testa i 3 esercizi implementati

def run_tests(G):
    years = [1960, 1970, 1980, 1990, 2000, 2010, 2020, 2023]

    # Test per la pubblicazione con il maggior numero di autori
    for year in years:
        publication, num_authors = find_publication_with_most_authors(G, year)
        print(f"Fino all'anno {year}, la pubblicazione con il maggior numero di autori è '{publication}' con {num_authors} autori.")

    print()

    # Test per le parole più comuni
    for year in years:
        common_words = find_most_common_word(G, year)
        print(f"Fino all'anno {year}, le parole più comuni nelle componenti con almeno 30 pubblicazioni sono:")
        for common_word in common_words:
            print(f" - '{common_word[0][0]}' appare {common_word[0][1]} volte")

    print()

    # Test per la pubblicazione con il maggior numero di autori popolari
    for year in years:
        publication, popularity_score = find_publication_with_most_popular_authors(G, year)
        print(f"Fino all'anno {year}, la pubblicazione con il maggior numero di autori popolari è '{publication}' con un punteggio di popolarità di {popularity_score}.")
    print()



################### Grafo 1 (article) ###################

# leggi il file .csv
df_1 = pd.read_csv('dblp-all-csv/out-dblp_article.csv', low_memory=False, delimiter=';')
# seleziona solo le colonne 'author', 'title' e 'year'
df_1 = df_1[['author', 'title', 'year']]
# Pulizia dei dati: rimuovere le righe con valori mancanti nelle colonne 'author' e 'title' e 'year'
df_1 = df_1.dropna(subset=['author', 'title', 'year'])
# separa gli autori in una lista
df_1['author'] = df_1['author'].apply(lambda x: x.split('|'))

print(df_1)

G_1 = nx.Graph()
G_1 = create_graph_from_df(G_1, df_1)  # crea il grafo dal dataframe

run_tests(G_1)


################## Grafo 2 (book) ###################

df_2 = pd.read_csv('dblp-all-csv/out-dblp_book.csv', low_memory=False, delimiter=';')
df_2 = df_2[['author', 'title', 'year']]
df_2['year'] = df_2['year'].apply(check_year)
df_2 = df_2.dropna(subset=['author', 'title', 'year'])
df_2['author'] = df_2['author'].apply(lambda x: x.split('|'))

print(df_2)

G_2 = nx.Graph()
G_2 = create_graph_from_df(G_2, df_2)  # crea il grafo dal dataframe

# plt.figure(figsize=(8,5))
# pos = nx.spring_layout(G_2)  # posiziona i nodi in modo che non si sovrappongano
# nx.draw(G_2, pos, with_labels=True, node_size=500, node_color="skyblue", node_shape="o", alpha=0.5, linewidths=4)
# plt.show()

run_tests(G_2)

################### Grafo 3 (incollection) ###################

df_3 = pd.read_csv('dblp-all-csv/out-dblp_incollection.csv', low_memory=False, delimiter=';')
df_3 = df_3[['author', 'title', 'year']]
df_3 = df_3.dropna(subset=['author', 'title', 'year'])
df_3['author'] = df_3['author'].apply(lambda x: x.split('|'))

print(df_3)

G_3 = nx.Graph()
G_3 = create_graph_from_df(G_3, df_3)

# plt.figure(figsize=(8,5))
# pos = nx.spring_layout(G_3)  # posiziona i nodi in modo che non si sovrappongano
# nx.draw(G_3, pos, with_labels=True, node_size=500, node_color="skyblue", node_shape="o", alpha=0.5, linewidths=4)
# plt.show()

run_tests(G_3)

################### Grafo 4 (inproceedings) ###################

df_4 = pd.read_csv('dblp-all-csv/out-dblp_inproceedings.csv', low_memory=False, delimiter=';')
df_4 = df_4[['author', 'title', 'year']]
df_4 = df_4.dropna(subset=['author', 'title', 'year'])
df_4['author'] = df_4['author'].apply(lambda x: x.split('|'))

print(df_4)

G_4 = nx.Graph()
G_4 = create_graph_from_df(G_4, df_4)

# plt.figure(figsize=(8,5))
# pos = nx.spring_layout(G_4)  # posiziona i nodi in modo che non si sovrappongano
# nx.draw(G_4, pos, with_labels=True, node_size=500, node_color="skyblue", node_shape="o", alpha=0.5, linewidths=4)
# plt.show()


run_tests(G_4)

################### Grafo 5 (mastersthesis) ###################

df_5 = pd.read_csv('dblp-all-csv/out-dblp_mastersthesis.csv', low_memory=False, delimiter=';')
df_5 = df_5[['author', 'title', 'year']]
df_5 = df_5.dropna(subset=['author', 'title', 'year'])
df_5['author'] = df_5['author'].apply(lambda x: x.split('|'))

print(df_5)

G_5 = nx.Graph()
G_5 = create_graph_from_df(G_5, df_5)

# plt.figure(figsize=(8,5))
# pos = nx.spring_layout(G_5)  # posiziona i nodi in modo che non si sovrappongano
# nx.draw(G_5, pos, with_labels=True, node_size=500, node_color="skyblue", node_shape="o", alpha=0.5, linewidths=4)
# plt.show()

run_tests(G_5)

################### Grafo 6 (phdthesis) ###################

# leggi il file .csv
df_6 = pd.read_csv('dblp-all-csv/out-dblp_phdthesis.csv', low_memory=False, delimiter=';')
# seleziona solo le colonne 'author', 'title' e 'year'
df_6 = df_6[['author', 'title', 'year']]
# Pulizia dei dati: rimuovere le righe con valori mancanti nelle colonne 'author' e 'title' e 'year'
df_6 = df_6.dropna(subset=['author', 'title', 'year'])
# trasforma la colonna 'year' in un intero
df_6['year'] = df_6['year'].apply(check_year)
# separa gli autori in una lista
df_6['author'] = df_6['author'].apply(lambda x: x.split('|'))

print(df_6)

G_6 = nx.Graph()
G_6 = create_graph_from_df(G_6, df_6)

# plt.figure(figsize=(8,5))
# pos = nx.spring_layout(G_6)  # posiziona i nodi in modo che non si sovrappongano
# nx.draw(G_6, pos, with_labels=True, node_size=500, node_color="skyblue", node_shape="o", alpha=0.5, linewidths=4)
# plt.show()

run_tests(G_6)

################### Grafo 7 (proceedings) ###################

df_7 = pd.read_csv('dblp-all-csv/out-dblp_proceedings.csv', low_memory=False, delimiter=';')
# Pulisci le colonne 'author' e 'editor'
df_7['author'] = df_7['author'].apply(lambda x: x.split('|') if pd.notnull(x) else [])
df_7['editor'] = df_7['editor'].apply(lambda x: x.split('|') if pd.notnull(x) else [])
# Crea una nuova colonna che unisce gli autori e gli editor
df_7['authors_and_editors'] = df_7.apply(lambda row: row['author'] + row['editor'], axis=1)
df_7 = df_7[['authors_and_editors', 'title', 'year']]
# Rinomina la colonna per compatibilità con il resto del codice
df_7 = df_7.rename(columns={'authors_and_editors': 'author'})

print(df_7)

G_7 = nx.Graph()
G_7 = create_graph_from_df(G_7, df_7)


# plt.figure(figsize=(8,5))
# pos = nx.spring_layout(G_7)  # posiziona i nodi in modo che non si sovrappongano
# nx.draw(G_7, pos, with_labels=True, node_size=500, node_color="skyblue", node_shape="o", alpha=0.5, linewidths=4)
# plt.show()

run_tests(G_7)

################### Grafo Unito ###################
df_all = pd.concat([df_1, df_2, df_3, df_4, df_5, df_6, df_7], ignore_index=True)

print(df_all)

G_all = nx.Graph()
G_all = create_graph_from_df(G_all, df_all)

run_tests(G_all)



################### Grafo Autori ###################

def create_author_graph_from_df(G, df):
    for _, row in df.iterrows():
        authors = row['author']
        # Creiamo un edge per ogni coppia di autori in ogni pubblicazione
        for i in range(len(authors)):
            for j in range(i + 1, len(authors)):
                if G.has_edge(authors[i], authors[j]):
                    # se l'edge esiste già, incrementiamo il peso
                    G[authors[i]][authors[j]]['weight'] += 1
                else:
                    # altrimenti, creiamo un nuovo edge con peso 1
                    G.add_edge(authors[i], authors[j], weight=1)
    return G

def find_max_collaboration(G):
    max_weight = 0
    max_edge = None
    for u, v, data in G.edges(data=True):
        if data['weight'] > max_weight:
            max_weight = data['weight']
            max_edge = (u, v)
    return max_edge, max_weight


# Crea il grafo degli autori dal dataframe combinato
G_authors = nx.Graph()
G_authors = create_author_graph_from_df(G_authors, df_all)

# Trova la collaborazione più frequente
max_edge, max_weight = find_max_collaboration(G_authors)
print(f"Gli autori che hanno collaborato di più sono: {max_edge[0]} e {max_edge[1]}, con {max_weight} collaborazioni.")









