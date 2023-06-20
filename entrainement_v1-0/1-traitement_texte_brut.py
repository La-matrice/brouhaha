import pandas as pd
import csv
from concurrent.futures import ProcessPoolExecutor

def phrases_vers_mots(phrase_input):

    print("Début de l'identification...")

    dictionnaire = pd.read_csv('dictionnaire.txt', sep='|', header=None, skiprows=1, encoding='utf-8')
    dictionnaire[0] = dictionnaire[0].apply(lambda x: x.lower())

    phrase_input = phrase_input.lower().strip()
    mots_input = []
    affichage_phrase = ""
    k = len(phrase_input) + 1

    while k > 0:
        found = False
        i = min(27, k)  # 27 est le nombre maximum de caractères d'une expression
        while not found and i >= 1:
            match_index = dictionnaire[dictionnaire[0] == phrase_input[:i]].index.tolist()
            if match_index:
                found = True
                mot = dictionnaire.loc[match_index[0], 0]
                affichage_phrase = affichage_phrase + " " + mot
                mots_input.append([mot])

                # mettre à jour phrase_input
                if ' ' in phrase_input or "'" in phrase_input or "." in phrase_input:
                    phrase_input = phrase_input[len(mot):].strip()
                    k = len(phrase_input)
                else:
                    phrase_input = ''
                    k = 0
            else:
                i -= 1

            if i == 0:
                print(f"Certains mots sont introuvables dans le dictionnaire : {phrase_input}")
                k = 0
                break

    if found == True:
        phrase_output = "|".join([mots_input[k][0] for k in range(len(mots_input))])
        print(phrase_output)

        with open("mots_v2.txt", "a") as file:
            file.write(phrase_output + '\n')

if __name__ == '__main__':
    phrases = pd.read_csv("phrases_v2.txt", delimiter = "\t", header=None)
    #phrases_vers_mots(phrases[0][0])
    phrases_vers_mots("c'est un pas")

    #with ProcessPoolExecutor() as executor:
     #   executor.map(phrases_vers_mots, phrases[0])