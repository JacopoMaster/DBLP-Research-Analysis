# DBLP-Research-Analysis

**Nota:** Per eseguire correttamente il seguente progetto Python, è necessario scaricare alcuni file. Puoi ottenere i file dal seguente link: [Download dei file delle pubblicazioni](https://drive.google.com/file/d/1kiys5-N3YYV6EcbcfxptImE_zpCPFfTX/view?usp=sharing).

In alternativa, i file sono stati scaricati da DBLP e processati per ottenere il formato .csv utilizzando lo script **XMLToCSV.py**, disponibile qui: [https://github.com/ThomHurks/dblp-to-csv](https://github.com/ThomHurks/dblp-to-csv).

## Descrizione del progetto
Questo progetto Python si concentra sull'analisi delle pubblicazioni accademiche. Utilizza un insieme di dati di pubblicazioni accademiche in formato .csv ottenuto da DBLP.

## Dipendenze
Il progetto Python dipende dalle seguenti librerie:

- pandas
- networkx
- matplotlib
- nltk

Puoi installare queste librerie utilizzando il comando seguente:

```
pip install pandas networkx matplotlib nltk
```

## Descrizione del codice
Il codice è suddiviso in diverse sezioni:

- Import delle librerie
- Definizione di funzioni utili per la creazione del grafo e l'analisi dei dati
- Esercizio 1: Trovare la pubblicazione con il maggior numero di autori
- Esercizio 2: Trovare la parola più comune nelle pubblicazioni
- Esercizio 3: Trovare la pubblicazione con il maggior numero di autori popolari
- Funzione di test per i 3 esercizi implementati
- Creazione dei grafi per diverse categorie di pubblicazioni (article, book, incollection, inproceedings, mastersthesis, phdthesis, proceedings)
- Esecuzione dei test sui grafi creati
- Creazione di un grafo unificato utilizzando tutti i dati delle pubblicazioni
- Trovare la collaborazione massima tra autori nel grafo unificato

## Esecuzione del codice
Per eseguire il codice, segui i passaggi seguenti:

1. Scarica i file delle pubblicazioni accademiche dal link fornito all'inizio del file README.
2. Posiziona i file nella stessa cartella del file Python.
3. Esegui il codice Python utilizzando il tuo ambiente Python preferito.

**Nota:** Assicurati di avere tutte le dipendenze installate prima di eseguire il codice.

Seleziona uno dei seguenti comandi per eseguire il codice:

Esegui il codice completo per analizzare tutte le categorie di pubblicazioni:
```
python DBLP.py
```

Commenta/rimuovi le sezioni relative alle categorie di pubblicazioni non desiderate e esegui il codice specifico per una singola categoria di pubblicazioni. Ad esempio, per eseguire solo l'analisi delle pubblicazioni di tipo 'article', lascia solo la sezione "Grafo 1 (article)" e esegui il codice.

Dopo l'esecuzione del codice, otterrai i seguenti risultati:

- Esercizio 1: La pubblicazione con il maggior numero di autori.
- Esercizio 2: La parola più comune nelle pubblicazioni.
- Esercizio 3: La pubblicazione con il maggior numero di autori popolari.
- Collaborazione massima tra autori nel grafo unificato.
