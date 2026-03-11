import time
import pandas as pd
from collections import Counter
import unicodedata as ud
import re
import heapq
from pywebio.input import input, radio
from pywebio.output import put_text, put_html, put_markdown

def top_k_keywords(speeches, k):
    """
    Args:
        speeches: ένα λεξικό που περιέχει τις ομιλίες ανά έτος
        k: ο αριθμός των πιο σημαντικών λέξεων-κλειδιών που πρέπει να επιστραφούν

    Returns: τις κορυφαίες k λέξεις-κλειδιά ανά έτος, και τις κορυφαίες k λέξεις-κλειδιά συνολικά.
    """
    total_keywords = Counter({})
    keywords_per_year = {}
    for year in speeches:
        yearly_speeches = speeches[year]
        keywords_per_year[year] = Counter({})
        for speech in yearly_speeches:
            keywords = extract_keywords(speech)
            keywords_per_year[year].update(keywords)
        total_keywords.update(keywords_per_year[year])
        keywords_per_year[year] = heapq.nlargest(k, keywords_per_year[year], key=keywords_per_year[year].get)  # κρατάμε τα κορυφαία k λέξεις-κλειδιά χρησιμοποιώντας ένα max heap
    total_keywords = heapq.nlargest(k, total_keywords, key=total_keywords.get)  # κρατάμε τα κορυφαία k λέξεις-κλειδιά χρησιμοποιώντας ένα max heap
    return keywords_per_year, total_keywords


def extract_keywords(speech):
    """
     Args:
        speech: μια ομιλία

    Returns: λέξεις-κλειδιά από μια συγκεκριμένη ομιλία και πόσες φορές εμφανίζεται κάθε λέξη.
    """
    result = re.sub("[^\w]", " ", speech).split()
    dict_counter = Counter(list(result))
    return dict_counter


def extract_only_keywords(speech):
    """
     Args:
        speech: μια ομιλία

    Returns: λέξεις-κλειδιά από μια συγκεκριμένη ομιλία
    """
    result = re.sub("[^\w]", " ", speech).split()
    return result


def find_speech(number_of_speech, number_of_rows, df):
    """

    Args:
        number_of_speech: ο αριθμός της ομιλίας που αναζητούν
        df: οι εγγραφές της ελληνικής βουλής
        number_of_rows: αριθμός των γραμμών που έχει το df

    Returns: μια συγκεκριμένη ομιλία

    """

    speech = {}
    number_of_speeches = 0
    if 0 <= number_of_speech < number_of_rows:
        year = df['sitting_date'][number_of_speech][-4:]
        speech[year] = [df['speech'][number_of_speech]]
        number_of_speeches = 1
    return speech, number_of_speeches


def find_speeches(df, name, category, number_of_rows):
    """

    Args:
        df: οι εγγραφές της ελληνικής βουλής
        number_of_rows: αριθμός των γραμμών που έχει το df
        name: το όνομα του βουλευτή ή του κόμματος για το οποίο αναζητούνται οι ομιλίες
        category: politician_party ή member_name (εξαρτάται από το τι αναζητούν)

    Returns: όλες οι ομιλίες ενός συγκεκριμένου κατηγορίας και πόσες είναι

    """
    name = name.lower()
    d = {ord('\N{COMBINING ACUTE ACCENT}'): None}  # αφαιρούμε τόνους
    name = ud.normalize('NFD', name).translate(d)
    speeches = {}
    number_of_speeches = 0
    last_year = '0'
    for i in range(number_of_rows):
        if df[category][i] == name:
            year = df['sitting_date'][i][-4:]  # έτος της ομιλίας
            if last_year < year:
                speeches[year] = []
                last_year = year
            speeches[year].append(df['speech'][i])  # αποθηκεύουμε την ομιλία σε ένα λεξικό ανά έτος ομιλίας
            number_of_speeches += 1
    return speeches, number_of_speeches


def main(data_path):
    df = pd.read_csv(data_path)
    number_of_rows = df.shape[0]
    start = time.time()
    put_markdown("# **Εύρεση keywords**")
    choice = radio("Θέλεις να βρεις λέξεις-κλειδιά: ", options=['ανά ομιλία', 'ανά βουλευτή', 'ανά κόμμα'])
    if choice == 'ανά ομιλία':  # εύρεση λέξεων-κλειδιών από μια συγκεκριμένη ομιλία
        number_of_speech = int(
            input('Δώσε αριθμό ομιλίας, μπορεί να είναι από το 0-' + str(number_of_rows - 1) + ' ', type='text'))
        speeches, number_of_speeches = find_speech(number_of_speech, number_of_rows, df)
    elif choice == 'ανά βουλευτή':  # εύρεση λέξεων-κλειδιών από όλες τις ομιλίες ενός πολιτικού
        member_name = input('Δώσε όνομα βουλευτή ', type='text')
        speeches, number_of_speeches = find_speeches(df, member_name, 'member_name', number_of_rows)
    else:  # εύρεση λέξεων-κλειδιών από όλες τις ομιλίες ενός πολιτικού κόμματος
        party_name = input('Δώσε όνομα κόμματος ', type='text')
        speeches, number_of_speeches = find_speeches(df, party_name, 'political_party', number_of_rows)

    put_markdown('# **Αποτελέσματα**')  # εκτύπωση αποτελεσμάτων
    put_text("Βρέθηκαν", number_of_speeches, "ομιλίες")
    put_html("<br>")
    if number_of_speeches == 0:
        put_text("Δεν βρέθηκαν ομιλίες")
        return

    k = int(input('Πόσες λέξεις-κλειδιά θες να σου επιστραφούν;', type='text'))
    keywords_per_year, keywords = top_k_keywords(speeches, k)
    end = time.time()

    put_html("<b>Λέξεις-κλειδιά: </b>")
    text = keywords[0]
    for i in range(1, len(keywords)):
        text += ", " + keywords[i]
    put_text(text + ".")
    put_html("<br>")

    if number_of_speeches > 1:
        put_html("<b>Λέξεις-κλειδιά ανά έτος: </b> <br> ")
        for year in keywords_per_year:
            put_html("<b>" + year + "</b>")
            text = keywords_per_year[year][0]
            for i in range(1, len(keywords_per_year[year])):
                text += ", " + keywords_per_year[year][i]
            put_text(text + ".")
            put_html("<br>")
    put_text("Χρόνος εκτέλεσης: " + f"{round(end - start, 2)} sec.\n")
