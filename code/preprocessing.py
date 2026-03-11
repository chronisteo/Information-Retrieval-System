import spacy
import string
import csv
import pandas as pd


def remove_stopwords(df, nlp, s):
    """ Αφαίρεση όλων των stop words και της στίξης από
    όλες τις ομιλίες στο csv αρχείο.

    Αποθήκευση της νέας μορφής των ομιλιών σε ένα νέο αρχείο,το "Proceedings_Processed.csv".

    Παράμετροι:
        df : το csv αρχείο
        nlp : spaCy's greek tokenizer
        s: δείκτης που δείχνει σε συγκεκριμένη ομιλία στο df

    """

    stop_words = nlp.Defaults.stop_words
    stop_words.update({'κ.', 'κύριος', 'κυρία', 'λόγο', 'συνάδελφος', 'επιτροπή', 'βουλευτής', 'υπουργός',
                       'δικαιοσύνη', 'διαδικασία', 'κυβέρνηση', 'βουλή', 'πρόεδρος', 'υπουργείο', 'πολιτικός'})
    #  αντικατάσταση στίξης με space
    new_speech = df['speech'][s].translate(str.maketrans(' ', ' ', string.punctuation))

    # αντικατάσταση stopwords με space
    for word in new_speech.split(' '):
        if word in stop_words:
            if (" " + word + " ") in new_speech:
                new_speech = new_speech.replace(" " + word + " ", " ")
            elif (word + " ") in new_speech:
                new_speech = new_speech.replace(word + " ", " ")
            elif (" " + word) in new_speech:
                new_speech = new_speech.replace(" " + word, " ")
    return new_speech


def keep_noun_propn_adj(nlp, speech):
    """

    Παράμετροι:
        nlp : spaCy's greek tokenizer
        speech: μία ομιλία αποθηκευμένη σε ένα string

    Επιστρέφει: τα ουσιαστικά,ονομάτα και
    απο μία ομιλία με αποκομμένες καταλήξεις.

    """

    pos_tag = ['PROPN', 'NOUN', 'ADJ']
    result = []
    doc = nlp(speech)

    for token in doc:
        if token.pos_ in pos_tag:
            result.append(token.lemma_)
    new_speech = ' '.join(result)
    return new_speech


def preprocessing():
    """ Αφαίρεση stopwords και στίξης,
   μετατροπή κάθε λέξης σε μικρά,διατήρηση όλων των ουσιαστικών,
   ονομάτων και επιθέτων από ολες τις ομιλίες με αποκομμένες καταλήξεις
   απο το csv αρχείο.

   Αποθήκευση του νέου φορμάτ των ομιλίων στο "Proceedings_Processed.csv".


   """

    data_path = '../data/Proceedings_1989_2020.csv'
    nlp = spacy.load("el_core_news_sm")

    df = pd.read_csv(data_path)
    number_of_rows = df.shape[0]

    # θέτουμε header του νέου csv αρχείου
    header = ['member_name', 'sitting_date', 'parliamentary_period', 'parliamentary_session', 'political_party',
              'government', 'roles', 'member_gender', 'speech']

    data = []

    for s in range(number_of_rows):
        # δημιουργία μίας λίστας με όλα τα στοιχεία μέσα
        # στήλη μίας γραμμής στο csv αρχείο
        data_row = []

        # αφαίρεση εγγραφών που έχουν NaN σε βασικά χαρακτηριστικά (member_name, politician_party, speech)
        if str(df['member_name'][s]) == 'nan' or str(df['political_party'][s]) == 'nan' or str(df['speech'][s]) == 'nan':
            break

        data_row.append(df['member_name'][s])
        data_row.append(df['sitting_date'][s])
        data_row.append(df['parliamentary_period'][s])
        data_row.append(df['parliamentary_session'][s])
        data_row.append(df['political_party'][s])
        data_row.append(df['government'][s])
        data_row.append(df['roles'][s])
        data_row.append(df['member_gender'][s])

        # αφαίρεση stopwords
        new_speech = remove_stopwords(df, nlp, s)

        # μικρά
        new_speech = new_speech.lower()

        # διατήρηση μόνο ουσιαστικών,ονομάτων και επιθέτων και εφαρμογή stemming
        new_speech = keep_noun_propn_adj(nlp, new_speech)

        data_row.append(new_speech)
        data.append(data_row)

    # Αποθήκευση των νέων δεδομέων στο csv αρχείο
    with open('../data/Proceedings_1989_2020_Processed.csv', 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)