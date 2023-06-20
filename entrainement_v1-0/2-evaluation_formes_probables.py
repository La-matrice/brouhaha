import pandas as pd
import csv
from concurrent.futures import ProcessPoolExecutor

def processus_phrases(phrase_input, phrases):

    plafond = 50
    affichage_phrase = ""

    print("Début de l'identification...")

    #phrases = pd.read_csv("mots.txt", delimiter = "\t", header=None)
    dictionnaire = pd.read_csv('dictionnaire.txt', sep='|', header=None, skiprows=1, encoding='utf-8')
    dictionnaire[0] = dictionnaire[0].apply(lambda x: x.lower())

    mots_input = []
    phrase_input = phrase_input.lower().strip()
    mots_phrase = pd.DataFrame(phrase_input.strip('|').split('|'))

    for index, row in mots_phrase.iterrows():
        mot_phrase = row[0]
        match_index = dictionnaire[dictionnaire[0] == mot_phrase].index.tolist()
        if match_index:
            found = True
            mot = dictionnaire.loc[match_index[0], 0]
            affichage_phrase = affichage_phrase + " " + mot
            id_ = dictionnaire.loc[match_index[0], 1]
            cv = dictionnaire.loc[match_index[0], 2]
            freq = dictionnaire.loc[match_index[0], 6]

            # Ajoute les résultats à la liste de résultats
            mots_input.append([mot, id_, '', '', '', '', cv, freq])
        else:
            print(f"Certains mots sont introuvables dans le dictionnaire : {mot_phrase}")
            print("Arrêt...")
            break
            found = False

    affichage_phrase = affichage_phrase.strip()
    print(affichage_phrase)
    print("Identification terminée !")

    if found == True:
        print("Début de l'évaluation des formes...")
        en_cours = pd.DataFrame(mots_input, columns=['Mot', 'ID', 'ID principal probable', '% ID principal', 'ID précis probable', '% ID précis probable', 'CV', 'Fréquence'])
        limite = len(mots_input)

        # tester chaque mot
        for k in range(limite):
            j = 1
            pourcentage_forme_principale = 0
            portion = ""
            best_score = 0
            formes_probables_principales = []
            formes_probables = []

            # si le mot possède plusieurs formes, évaluer sa forme
            if "&" in mots_input[k][1]:
                print("Le mot suivant possède plusieurs formes :",mots_input[k][0])

                if limite == 1:
                    print(f"Le mot {mots_input[k][0]} comporte plusieurs formes, merci de saisir plus d'un mot pour lancer la génération !")
                    exit()

                # tester 4 positions différentes (de n+1, n+2 à n-1, n-2) et identifier le mot indice
                for position in range(4):
                    compteur = 0
                    if position < 2:
                        if k + (position + 1) < limite:
                            indice = mots_input[k + (position + 1)][0]
                        else:
                            continue
                    else:
                        if k - (position - 1) > - 1:
                            indice = mots_input[k - (position - 1)][0]
                        else:
                            continue

                    # rechercher uniquement les lignes qui contiennent l'indice
                    lignes_phrases = phrases[phrases[0].str.contains(indice)]

                    # tester chaque ligne du fichier 'mots'
                    for index, row in lignes_phrases.head(plafond).iterrows():
                        ligne_phrase = row[0]
                        ligne_phrase = pd.DataFrame(ligne_phrase.strip('|').split('|'))

                        contains_indice = ligne_phrase[0].str.contains(indice)
                        positions_indice = contains_indice.where(contains_indice==True).dropna().index.tolist()

                        z = ligne_phrase.shape[0]

                        for position_indice in positions_indice:

                            if ligne_phrase[0][position_indice] == indice:

                                x = position_indice

                                # relever la portion de la ligne correspondante
                                if position <= 1:
                                    if x - (position + 1) > 0:
                                        portion = ligne_phrase[0][x - (position + 1)]
                                    else:
                                        break
                                else:
                                    if x + (position - 1) < z:
                                        portion = ligne_phrase[0][x + (position - 1)]
                                    else:
                                        break

                                # rechercher la ligne du dictionnaire qui contient la portion
                                lignes_dictionnaire = dictionnaire[dictionnaire[0] == portion]
                                formes_dictionnaire = []
                                formes_dictionnaire = lignes_dictionnaire[1].str.split(' & ').explode().tolist()
                                m = 0
                                n = len(formes_dictionnaire)

                                liste_doublons = []

                                # calculer le nombre de formes probables du mot trouvé
                                for forme_dictionnaire in formes_dictionnaire:

                                    compteur += 1

                                    # saisir les formes probables principales et formes probables précises ainsi que leur nombre d'occurrence
                                    forme = forme_dictionnaire
                                    forme_principale = forme[:3]
                                    doublon = forme_principale in liste_doublons

                                    # Saisie de la forme précise
                                    for forme_probable in formes_probables:
                                        if forme == forme_probable[0]:
                                            forme_probable[position + 1] += 1
                                            break
                                    else:
                                        ligne = ["", 0, 0, 0, 0]
                                        ligne[0] = forme
                                        ligne[position + 1] += 1
                                        formes_probables.append(ligne)

                                    # saisir la forme principale
                                    # vérifier qu'il n'y a pas de doublon de forme principale pour le même mot
                                    if not doublon:
                                        liste_doublons.append(forme_principale)

                                        # si pas de doublon, saisir le nombre d'occurrence
                                        for forme_probable_principale in formes_probables_principales:
                                            if forme_principale == forme_probable_principale[0]:
                                                forme_probable_principale[position + 1] += 1
                                                break
                                        else:
                                            ligne = ["", 0, 0, 0, 0]
                                            ligne[0] = forme_principale
                                            ligne[position + 1] += 1
                                            formes_probables_principales.append(ligne)
                                    m += 1

                # calculer la moyenne des positions par forme principale
                for position in range(1, 5):
                    compteur = 0
                    pourcentage = 0
                    i = 0
                    while i < len(formes_probables_principales) and formes_probables_principales[i][0] != "":
                        compteur += 1
                        if formes_probables_principales[i][position] > 0:
                            pourcentage += formes_probables_principales[i][position]
                        i += 1

                    # saisir le pourcentage de présence d'une forme pour chaque position
                    for i in range(compteur):
                        if formes_probables_principales[i][position] > 0:
                            formes_probables_principales[i][position] = (formes_probables_principales[i][position] * 100) / pourcentage

                # saisir la moyenne
                for i in range(compteur):
                    pourcentage = 0
                    for position in range(1, 5):
                        pourcentage += formes_probables_principales[i][position]
                    formes_probables_principales[i][1] = pourcentage / 4

                # trier les formes_probables_principales par ordre décroissant des moyennes
                formes_probables_principales.sort(key=lambda x: x[1], reverse=True)

                # attribuer la forme principale la plus probable
                compteur = mots_input[k][1].count("&")
                pourcentage = 0
                best_forme = 0
                for i in range(compteur + 1):
                    j = 0
                    while j < len(formes_probables_principales):
                        id_unique = mots_input[k][1].split("&")[i].strip()[:3]  # 3 pour uniquement connaitre la forme principale
                        if id_unique == formes_probables_principales[j][0]:
                            if pourcentage < formes_probables_principales[j][1]:
                                best_forme = mots_input[k][1].split("&")[i].strip()
                                pourcentage = formes_probables_principales[j][1]
                                mots_input[k][2] = formes_probables_principales[j][0]
                                mots_input[k][3] = pourcentage
                                pourcentage_forme_principale = pourcentage
                        j += 1

                # si aucune forme similaire trouvée du mot input en cours, attribuer la forme la plus probable
                if best_forme == 0:
                    print("Aucune forme principale similaire trouvée...")
                    mots_input[k][2] = formes_probables_principales[0][0]
                    mots_input[k][3] = formes_probables_principales[0][1]

                # calculer la moyenne des positions par forme précise à partir de la forme principale la plus probable
                for position in range(1, 5):
                    compteur = 0
                    pourcentage = 0
                    i = 0
                    while i < len(formes_probables):
                        compteur += 1
                        if formes_probables[i][0][:3] == mots_input[k][2]:
                            if formes_probables[i][position] > 0:
                                pourcentage += formes_probables[i][position]
                        else:
                            for p in range(1, 5):
                                formes_probables[i][p] = 0
                        i += 1

                    # saisir le pourcentage de présence d'une forme pour chaque position
                    for i in range(compteur):
                        if formes_probables[i][position] > 0:
                            formes_probables[i][position] = (formes_probables[i][position] * 100) / pourcentage

                # saisir la moyenne
                for i in range(compteur):
                    pourcentage = 0
                    for position in range(1, 5):
                        pourcentage += formes_probables[i][position]
                    formes_probables[i][1] = pourcentage / 4

                # trier les formes probables par ordre décroissant des moyennes
                formes_probables.sort(key=lambda x: x[1], reverse=True)

                # attribuer la forme la plus probable
                compteur = mots_input[k][1].count("&")
                pourcentage = 0
                for i in range(compteur + 1):
                    j = 0
                    while j < len(formes_probables) and formes_probables[j][0] != "":
                        id_unique = mots_input[k][1].split("&")[i].strip()
                        if id_unique == formes_probables[j][0]:
                            if pourcentage < formes_probables[j][1]:
                                best_forme = mots_input[k][1].split("&")[i].strip()
                                best_score = formes_probables[j][1]
                                pourcentage = formes_probables[j][1]
                        j += 1

                # si aucune forme similaire trouvée du mot input en cours, attribuer la forme la plus probable
                if best_forme == 0:
                    print("Aucune forme précise similaire trouvée...")
                    mots_input[k][2] = formes_probables[0][0]
                    mots_input[k][3] = formes_probables[0][1]
                else:

                    mots_input[k][4] = best_forme
                    mots_input[k][5] = best_score

                print("   Nouvelle forme attribuée : ", mots_input[k][4])

            # si le mot dispose que d'une seule forme
            else:
                mots_input[k][2] = mots_input[k][1][:3]
                mots_input[k][3] = "100"
                mots_input[k][4] = mots_input[k][1]
                mots_input[k][5] = "100"
                mots_input[k][6] = cv
                mots_input[k][7] = freq

        phrase_output = "|".join([mots_input[k][4] for k in range(limite)])
        print(phrase_output)

        with open("silence_v2.txt", "a") as file:
            file.write(phrase_output + '\n')

if __name__ == '__main__':

    phrases = pd.read_csv("mots.txt", delimiter = "\t", header=None)
    #processus_phrases(phrases[0][0], phrases)
    processus_phrases("c'est un pas")

    #with ProcessPoolExecutor() as executor:
     #   executor.map(processus_phrases, phrases[0], phrases)
