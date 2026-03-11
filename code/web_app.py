from pywebio import start_server
from pywebio.input import input, radio, select
import keywords
import tf_idf
import lsi
import extra

#data_path = '../data/Proceedings_1989_2020_Processed.csv'
#data_path = '../data/Proceedings_100000_Processed.cσsv'
data_path = '../data/Proceedings_Processed.csv'


def webapp_main():
    #Με την επιλογή αυτή βρίσκουμε ανά ομιλία, ανά βουλευτή και ανά κόμμα,
    #τις σημαντικότερες λέξεις-κλειδιά
    #και πως αυτές αλλάζουν στο χρόνο.
    opt_keywords = 'Σημαντικότερες λέξεις-κλειδιά'

    #Με την επιλογή αυτή βρίσκουμε
    #τα top-k ζεύγη με τον υψηλότερο βαθμό ομοιότητας
    opt_tf_idf = 'Τop-k ζεύγη με τον υψηλότερο βαθμό ομοιότητας'

    #Με την επιλογή αυτή βρίσκουμε τις σημαντικότερες θεματικές περιοχές
    #και εκφράσουμε την κάθε ομιλία ως διάνυσμα σε κάποιον πολυδιάστατο χώρο
    opt_lsi = 'Σημαντικότερες θεματικές περιοχές'

    #Η επιπλέον ιδεά προς υλοποίηση, η οποία ανιχνέυει
    #ομοιότητες μεταξύ διαφόρων θεματικών περιοχών
    opt_extra = 'Ομοιότητες μεταξύ θεματικών περιοχών'

    mode = radio("Αναζήτηση", options=[opt_keywords, opt_tf_idf , opt_lsi, opt_extra])

    if mode == opt_keywords:
        keywords.main(data_path)
    elif mode == opt_tf_idf:
        tf_idf.main(data_path)
    elif mode == opt_lsi:
        lsi.main(data_path)
    elif mode == opt_extra:
        extra.main(data_path)



if __name__ == '__main__':
    start_server(webapp_main, port=8080, debug=True)




