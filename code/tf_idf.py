import csv
from pywebio.output import put_text, put_markdown
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import heapq
import time
from pywebio.input import input
import os.path


def main(data_path):

    k = int(input('Πόσα top-k θες να σου επιστραφούν;', type='text'))

    start = time.time()
    data_tf_idf_path = '../data/Proceedings_1989_2020_Processed_tf_idf.csv'
    if not os.path.isfile(data_tf_idf_path):
        preprocessing(data_path)

    df = pd.read_csv(data_tf_idf_path)
    number_of_rows = df.shape[0]

    # εδώ ορίζουμε τη συλλογή των εγγράφων μας
    # αυτό είναι ένας πίνακας από συμβολοσειρές
    documents = []
    for i in range(number_of_rows):
        documents.append(df['Speeches'][i])

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # ορίζουμε τον πίνακα ομοιότητας εγγράφων-εγγράφων με βάση την απόσταση cosine
    ddsim_matrix = cosine_similarity(tfidf_matrix[:], tfidf_matrix)

    heap = []
    # δημιουργούμε ένα max heap που περιέχει τα top-k σκορ tf-idf
    for i in range(number_of_rows):
        for j in range(i + 1, number_of_rows):
            # Αν δεν έχουμε βρει ακόμα k στοιχεία, ή το τρέχον στοιχείο είναι μεγαλύτερο από το μικρότερο στοιχείο στο heap
            if len(heap) < k or ddsim_matrix[i][j] > heap[0][0]:
                # Αν το heap είναι γεμάτο, αφαιρούμε το μικρότερο στοιχείο
                if len(heap) == k:
                    heapq.heappop(heap)
                # προσθέτουμε το τρέχον στοιχείο ως το νέο μικρότερο
                heapq.heappush(heap, [ddsim_matrix[i][j], i, j])

    put_markdown('# **Αποτελέσματα**')  # εκτύπωση αποτελεσμάτων
    put_markdown("# **Top-" + str(k) + "** ")
    for i in range(len(heap)):
        put_text(df['Name'][heap[i][1]].upper(), " - ", df['Name'][heap[i][2]].upper())
    end = time.time()
    put_text("Χρόνος εκτέλεσης: " + f"{round(end - start, 2)} sec.\n")


def preprocessing(data_path):
    df = pd.read_csv(data_path)
    number_of_rows = df.shape[0]
    members_speeches = {}
    for i in range(number_of_rows):
        name = str(df['member_name'][i])
        speech = str(df['speech'][i])
        if name in members_speeches:
            members_speeches[name] += " " + speech
        else:
            members_speeches[name] = " "

    header = ['Name', 'Speeches']
    csv_file = '../data/Proceedings_1989_2020_Processed_tf_idf.csv'
    try:
        with open(csv_file, 'w', encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for key, value in members_speeches.items():
                writer.writerow([key, value])
    except IOError:
        print("I/O error")




