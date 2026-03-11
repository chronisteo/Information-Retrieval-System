import time
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from pywebio.output import put_text, put_markdown, put_html
from pywebio.input import input, radio


# data_path = '../data/Proceedings_1989_2020_Processed.csv'
# data_path = '../data/Proceedings_Processed.csv'

def main(data_path):
    df = pd.read_csv(data_path)
    number_of_rows = df.shape[0]

    num_of_topics = int(input('Πόσες θεματικές περιοχές θέλεις να εμφανιστούν;', type='text'))

    start = time.time()

    processed_list = []
    for s in range(number_of_rows):
        processed_list.append(str(df['speech'][s]))

    """
    Χρήση του TfidfVectorizer από τη βιβλιοθήκη scikit-learn 
    για μετατροπή των κειμένων σε μια αναπαράσταση με τη 
    μέθοδο TF-IDF
    """
    vect = TfidfVectorizer()
    tfidf_matrix = vect.fit_transform(processed_list)

    """
        Χρήση του TruncatedSVD για εκτέλεση της 
        μεθόδου της Κυρτής Συνθλιβόμενης Εκκοπής (Truncated Singular Value Decomposition - LSA) πάνω στο πίνακα TF-IDF 
        και εξαγωγή των σημαντικών θεματικών περιοχών    """

    lsa_model = TruncatedSVD(n_components=num_of_topics, n_iter=num_of_topics)

    lsa_top = lsa_model.fit_transform(tfidf_matrix)
    l = lsa_top[0]

    terms = vect.get_feature_names_out()

    put_markdown('# **Αποτελέσματα**')  # εκτύπωση αποτελεσμάτων
    put_markdown("# **Οι-" + str(num_of_topics) + " σημαντικότερες θεματικές περιοχές ** ")

    # σημαντικές λέξεις
    for i, component in enumerate(lsa_model.components_):
        zipped = zip(terms, component)
        terms_key = sorted(zipped, key=lambda t: t[1], reverse=True)[:num_of_topics]
        terms_list = list(dict(terms_key).keys())
        put_text("Θεματική Περιοχή " + str(i) + ": ", terms_list)

    put_markdown("# **Οι διανυσματικές αναπαραστάσεις των σημαντικότερων θεματικών περιοχών ** ")

    # διανυσματική αναπαράσταση
    for i, topic in enumerate(l):
        put_text("Θεματική Περιοχή ", i, " : ", topic * 100)
        put_text(lsa_model.components_)
        put_text("\n")

    end = time.time()
    put_text("Χρόνος εκτέλεσης: " + f"{round(end - start, 2)} sec.\n")