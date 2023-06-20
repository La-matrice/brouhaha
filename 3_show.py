import pandas as pd
import csv
import random

indice_creativite = 10
phrase = ""
mots_input= []

def load_data():
    df = pd.read_csv('logs.txt', sep="|", header=None, encoding='utf-8')
    for index, row in df.iterrows():
        mot = row[0]
        id_ = row[1]
        idp = row[2]
        idpp = row[3]
        ide = row[4]
        idep = row[5]
        cv = row[6]
        freq = row[7]
        mots_input.append([mot, id_,  idp , idpp, ide , idep , cv, freq])
    return mots_input

def get_probable_words(mots_input, CV):
    with open('/content/drive/MyDrive/brouhaha_save/dictionnaire.txt', 'r', encoding="utf-8") as file2:
        reader = csv.reader(file2, delimiter='|')
        mots_probables = []
        for row in reader:
            if forme_probable in row[1]:
                if CV == "C":
                    if row[2][1] == "C":
                        mots_probables.append(row)
                else:
                    mots_probables.append(row)
    return mots_probables

def get_random_word(mots_probables):
    mots_probables = sorted(mots_probables, key=lambda row: row[6], reverse=True)
    x = random.randint(1, indice_creativite)
    if x > len(mots_probables):
        x = len(mots_probables)
    mot_choisi = mots_probables[x - 1][0]
    formes_probables = mots_probables[x - 1][1]
    cv_choisi = mots_probables[x - 1][2]
    frequence = mots_probables[x - 1][6]
    return mot_choisi, formes_probables, cv_choisi, frequence

def update_mots_input(mots_input, mot_choisi, formes_probables, cv_choisi, frequence):
    mots_input.pop()
    nouvelle_ligne = [mot_choisi] + [0] * (7)
    mots_input.append(nouvelle_ligne)
    mots_input[-1][1] = formes_probables
    mots_input[-1][2] = forme_principale
    mots_input[-1][3] = pourcentage_forme_principale
    mots_input[-1][4] = forme_probable
    mots_input[-1][5] = pourcentage_forme_probable
    mots_input[-1][6] = cv_choisi
    mots_input[-1][7] = frequence
    return mots_input

def save_data(mots_input):
    with open('logs.txt', "w", encoding='utf-8', newline="") as fichier:
        writer = csv.writer(fichier, delimiter='|')
        writer.writerows(mots_input)

def format_phrase(mots_input):
    for line in mots_input:
        phrase = " ".join(sublist[0] for sublist in mots_input)
    phrase = phrase.replace(" , ", ", ")
    phrase = phrase.replace("' ", "'")
    phrase = phrase.replace(" .", ".")
    return phrase
  
# Main function to run everything
def main():
    mots_input = load_data()
    CV = determine_cv(mots_input)
    mots_probables = get_probable_words(mots_input, CV)
    if len(mots_probables) == 0:
        mots_probables = get_probable_words_without_cv_filter(mots_input)
    mot_choisi, formes_probables, cv_choisi, frequence = get_random_word(mots_probables)
    mots_input = update_mots_input(mots_input, mot_choisi, formes_probables, cv_choisi, frequence)
    save_data(mots_input)
    phrase = format_phrase(mots_input)
    print(phrase)

# Call the main function
main()
