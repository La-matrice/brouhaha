import customtkinter as ctk
import pandas as pd
import random
import csv

#----------------------------------------------------------------------------------------------------------------------------------------------------

def processus_phrases(phrase_input):

    print("Début de l'identification...")

    plafond = 100

    dictionnaire = pd.read_csv('dictionnaire.txt', sep='|', header=None, skiprows=1, encoding='utf-8')
    dictionnaire[0] = dictionnaire[0].apply(lambda x: x.lower())
    phrases = pd.read_csv("mots.txt", delimiter = "\t", header=None)
    phrase_input = phrase_input.lower().strip()
    k = len(phrase_input) + 1
    mots_input = []
    affichage_phrase = ""

    # boucler jusqu'à trouver toutes les expressions
    while k > 0:
        found = False
        i = min(27, k)  # 27 est le nombre maximum de caractères d'une expression du dictionnaire

        while not found:
            match_index = dictionnaire[dictionnaire[0] == phrase_input[:i]].index.tolist()

            if match_index:
                found = True
                mot = dictionnaire.loc[match_index[0], 0]
                affichage_phrase = affichage_phrase + " " + mot
                id_ = dictionnaire.loc[match_index[0], 1]
                cv = dictionnaire.loc[match_index[0], 2]
                freq = dictionnaire.loc[match_index[0], 6]
                mots_input.append([mot, id_, '', '', '', '', cv, freq])

                # décrémenter phrase_input
                if ' ' in phrase_input or "'" in phrase_input:
                    phrase_input = phrase_input[len(mot):].strip()
                    k = len(phrase_input)
                else:
                    phrase_input = ''
                    k = 0
            else:
                i -= 1

            # si aucune expression n'est trouvée, arrêter le programme
            if i == 0:
                print(f"Certains mots sont introuvables dans le dictionnaire : {phrase_input}")
                k = 0
                break

    affichage_phrase = affichage_phrase.strip()
    print(affichage_phrase)
    print("Identification terminée !")

    # évaluer la forme probable de chaque expression trouvée
    if found == True and i > 0:
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

                    # tester chaque ligne du fichier 'Mots'
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

                                # saisir les formes probables principales et formes probables précises ainsi que leur nombre d'occurrence
                                for forme_dictionnaire in formes_dictionnaire:
                                    compteur += 1
                                    forme = forme_dictionnaire
                                    forme_principale = forme[:3]
                                    doublon = forme_principale in liste_doublons

                                    # sasir la forme complète (forme la plus précise)
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
                                    # vérifier qu'il n'y a pas de doublon de forme principale pour cette même expression
                                    if not doublon:
                                        liste_doublons.append(forme_principale)

                                        # si pas de doublon saisir le nombre d'occurrence
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
                                #c = pourcentage
                                mots_input[k][2] = formes_probables_principales[j][0]
                                mots_input[k][3] = pourcentage
                                pourcentage_forme_principale = pourcentage
                        j += 1

                # si aucune forme similaire trouvée du mot input en cours, attribution de la forme principale la plus probable
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

                mots_input[k][4] = best_forme
                mots_input[k][5] = best_score

                # si aucune forme similaire trouvée du mot input en cours, attribution de la forme précise la plus probable
                if best_forme == 0:
                    print("Aucune forme précise similaire trouvée...")
                    mots_input[k][4] = formes_probables[0][0]
                    mots_input[k][5] = formes_probables[0][1]

                print("   Nouvelle forme attribuée : ", mots_input[k][4])

            # si le mot dispose que d'une seule forme
            else:
                mots_input[k][2] = mots_input[k][1][:3]
                mots_input[k][3] = "100"
                mots_input[k][4] = mots_input[k][1]
                mots_input[k][5] = "100"
                mots_input[k][6] = cv
                mots_input[k][7] = freq

        with open('logs.txt', "w", newline="") as fichier:
                writer = csv.writer(fichier, delimiter='|')
                writer.writerows(mots_input)

    print("Évaluation terminée !")
    
    prediction_forme()

#----------------------------------------------------------------------------------------------------------------------------------------------------

def prediction_forme():

    print("Début de la prédiction...")

    limite_prediction = 2000 # limite de recherche

    k = 0
    formes_input = []
    formes_precises_probables = []
    formes_principales_probables = []

    # Lecture du fichier
    logs = pd.read_csv('logs.txt', sep="|", header=None, encoding='utf-8')
    silence = pd.read_csv("silence.txt", delimiter = "\t", header=None)

    # Itération à travers les lignes
    for index, row in logs.iterrows():
        mot = row[0]
        id_ = row[1]
        idp = row[2]
        idpp = row[3]
        ide = row[4]
        idep = row[5]
        cv = row[6]
        freq = row[7]
        formes_input.append([mot, id_,  idp , idpp, ide , idep , cv, freq])
        k += 1

    x = len(formes_input) - 1 # Nombre total de forme
    p = 0

    output = []
    trouve = False
    reduction = False
    suite = False

    # boucler sur chaque formes_input jusqu'à trouver une probabilité
    while not trouve and p <= x:

        FiltreForme = 25
        partiel = False
        reduction = False
        recherche_suite = ""
        n = p
        for m in range(n, x + 1):
            recherche_suite = recherche_suite + " " + formes_input[m][4]
        print("Recherche de la suite:", recherche_suite, " avec le filtre:", FiltreForme)

        # continuer et réduire le filtre jusqu'à trouver une correspondance
        while partiel == False and FiltreForme > 3:

            print("Filtre actuel:", FiltreForme)
            filtre_recherche = pd.DataFrame()
            nombre_de_lignes = 0

            # rechercher uniquement les lignes qui contiennent la première forme de la suite à rechercher
            forme_recherche = formes_input[p][4][:FiltreForme]
            filtre_recherche = silence[silence[0].str.contains(forme_recherche)]

            for i in range(p + 1, x + 1):

                forme_recherche = formes_input[i][4][:FiltreForme]
                filtre_recherche = filtre_recherche[filtre_recherche[0].str.contains(forme_recherche)]

            nombre_de_lignes = filtre_recherche.shape[0]

            # si des lignes ont été trouvées, poursuivre l'évaluation
            if nombre_de_lignes > 0:

                # boucler sur l'ensemble des lignes filtrées et vérifier la correspondance de l'ordre des formes
                for index, row in filtre_recherche.head(limite_prediction).iterrows():
                    doublon_precedent = ""
                    ligne = row[0]
                    mots = ligne.split("|")  # sépare la ligne en mots
                    formes_par_mot = [mot.split(" & ") for mot in mots]
                    ligne_recherche = pd.DataFrame(formes_par_mot).transpose()
                    ligne_recherche = ligne_recherche.applymap(lambda x: x[:FiltreForme] if isinstance(x, str) else x)

                    # rechercher les positions de la première forme dans le tableau
                    cherche = ligne_recherche.isin([formes_input[p][4][:FiltreForme]])
                    colonnes = cherche.any()

                    for colonne in colonnes.index:
                        if colonnes[colonne] and colonne + x + 1 - p <= ligne_recherche.shape[1]:
                            suite = True
                            # une fois la position de la première forme trouvée, vérifier la correspondance des colonnes suivantes
                            for i in range(1, x + 1 - p):
                                if colonne + i <= len(ligne_recherche.columns) and ligne_recherche[colonne + i].isin([formes_input[p + i][4][:FiltreForme]]).any():
                                    ok = True
                                else:
                                    suite = False
                                    break

                            # si la suite est conforme, relever la forme suivante potentielle
                            if suite == True and colonne + x + 1 - p < len(ligne_recherche.columns):
                                partiel = True
                                formes_successives = ligne_recherche[colonne + x + 1 - p]
                                formes_successives = formes_successives.dropna()

                                  # vérifier et mettre à jour les formes_principales_probables
                                for ligne_forme in formes_successives:
                                    doublon = ligne_forme[:3]
                                    forme_existe = False
                                    if doublon != doublon_precedent:
                                        for i, forme_principale in enumerate(formes_principales_probables):
                                            if forme_principale[0][:3] == doublon:
                                                formes_principales_probables[i][x + 1 - p] += 1
                                                forme_existe = True
                                                break
                                        if not forme_existe:
                                            nouvelle_ligne = [doublon] + [0] * (x + 1)
                                            formes_principales_probables.append(nouvelle_ligne)
                                            formes_principales_probables[-1][x + 1 - p] += 1
                                    doublon_precedent = doublon

                                # Vérifier et mettre à jour les formes_precises_probables
                                if reduction == False:
                                    trouve = True
                                    for ligne_forme in formes_successives:
                                        forme_existe = False
                                        for i, forme_principale in enumerate(formes_precises_probables):
                                            if forme_principale[0] == ligne_forme:
                                                formes_precises_probables[i][p + 1] += 1
                                                forme_existe = True
                                                break

                                        if not forme_existe:
                                            nouvelle_ligne = [ligne_forme] + [0] * (x + 1)
                                            formes_precises_probables.append(nouvelle_ligne)
                                            formes_precises_probables[-1][p + 1] += 1
                        
            FiltreForme = FiltreForme - 1
            reduction = True
        p += 1

    # calculer la forme la plus probable
    sommes_colonne = []
    # calculer la moyenne des formes_principales_probables
    # calculerl a moyenne par colonne
    for i, col in enumerate(zip(*formes_principales_probables)):
        if i >= 1:
            sommes_colonne.append(sum(col))

    #  calculer les moyennes de chaque colonne
    moyennes_colonnes = []

    for ligne in formes_principales_probables:
        nouvelle_ligne = [ligne[0]]
        for i in range(1, len(ligne)):
            if sommes_colonne[i - 1] == 0:
                moyenne = 0
            else:
                # calculer la moyenne de la colonne
                moyenne = ligne[i] / sommes_colonne[i - 1]
                nouvelle_ligne.append(moyenne)
        moyennes_colonnes.append(nouvelle_ligne)

    # calculer la moyenne par ligne
    moyennes_ligne = []

    for ligne in moyennes_colonnes:
        moyenne_ligne = sum(ligne[1:]) / (len(ligne) - 1) 
        ligne.insert(1, moyenne_ligne  * 100)
        moyennes_ligne.append(ligne)

    # trier les moyennes par ordre décroissant en fonction de la deuxième colonne
    moyennes_ligne = sorted(moyennes_ligne, key=lambda x: x[1], reverse=True)

    # si qu'une seule forme précise n'est trouvée, attribuer la forme principale de la forme précise et le score de la forme principale correspondante
    forme_principale_unique = all(ligne[0].startswith(formes_precises_probables[0][0][:3]) for ligne in formes_precises_probables)

    if forme_principale_unique == True:
        print("Les formes précises probables ne font partie que d'une seule catégorie de forme principale...")
        for ligne in moyennes_ligne:
            if ligne[0] == formes_precises_probables[0][0][:3]:
                best_forme_principale = ligne[0]
                best_score_principal = ligne[1]
    else:
        best_forme_principale = moyennes_ligne[0][0]
        best_score_principal = moyennes_ligne[0][1]

    # calculer la moyenne des formes_precises_probables
    sommes_colonne = []

    formes_precises_probables = [ligne for ligne in formes_precises_probables if best_forme_principale in ligne[0][:3]]

    # calculer la moyenne par colonne
    for i, col in enumerate(zip(*formes_precises_probables)):
        if i >= 1:
            sommes_colonne.append(sum(col))
    moyennes_colonnes = []

    for ligne in formes_precises_probables:
        nouvelle_ligne = [ligne[0]]
        for i in range(1, len(ligne)):
            if sommes_colonne[i - 1] == 0:
                moyenne = 0
            else:
                # calculer la moyenne de la colonne
                moyenne = ligne[i] / sommes_colonne[i - 1]
                nouvelle_ligne.append(moyenne)
        moyennes_colonnes.append(nouvelle_ligne)

    # calculer la moyenne par ligne
    moyennes_ligne = []

    for ligne in moyennes_colonnes:
        moyenne_ligne = sum(ligne[1:]) / (len(ligne) - 1)
        ligne.insert(1, moyenne_ligne * 100)
        moyennes_ligne.append(ligne)

    # trier les moyennes obtenues par ordre décroissant en fonction de la deuxième colonne
    moyennes_ligne = sorted(moyennes_ligne, key=lambda x: x[1], reverse=True)

    best_forme_precise = moyennes_ligne[0][0]
    best_score_precis = moyennes_ligne[0][1]

    nouvelle_ligne = ['[...]'] + [0] * (7)
    formes_input.append(nouvelle_ligne)
    formes_input[-1][1] = best_forme_precise
    formes_input[-1][2] = best_forme_principale
    formes_input[-1][3] = best_score_principal
    formes_input[-1][4] = best_forme_precise
    formes_input[-1][5] = best_score_precis
    formes_input[-1][6] = 'XX'
    formes_input[-1][7] = 0

    with open('logs.txt', "w", encoding='utf-8', newline="") as fichier:
            writer = csv.writer(fichier, delimiter='|')
            writer.writerows(formes_input)

    #for line in formes_input:
    #    print(line)

    if formes_input[-1][4] == "PON:po":
        print("Phrase terminée...")
    else:
      print("Prédiction des formes terminée")    

    affichage_mot_probable()

#----------------------------------------------------------------------------------------------------------------------------------------------------
    
def affichage_mot_probable():

    indice_creativite = 10

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    phrase = ""
    mots_input= []
    logs = pd.read_csv('logs.txt', sep="|", header=None, encoding='utf-8')

    for index, row in logs.iterrows():
        mot = row[0]
        id_ = row[1]
        idp = row[2]
        idpp = row[3]
        ide = row[4]
        idep = row[5]
        cv = row[6]
        freq = row[7]

        mots_input.append([mot, id_,  idp , idpp, ide , idep , cv, freq])

    forme_principale = mots_input[-1][2]
    pourcentage_forme_principale = mots_input[-1][3]
    forme_probable = mots_input[-1][4]
    pourcentage_forme_probable = mots_input[-1][5]
    CV = ""

    if mots_input[-2][6][-1] == "V":
      CV = "C"
    else:
      CV = "V"

    with open('dictionnaire.txt', 'r', encoding="utf-8") as dictionnaire:
        ligne_dictionnaire = csv.reader(dictionnaire, delimiter='|')
        mots_probables = []

        # parcourir chaque ligne du dictionnaire
        for row in ligne_dictionnaire:
            if forme_probable in row[1]:
                # vérifier si le mot probable doit commencer par une consonne
                if CV == "C":
                    if row[2][1] == "C":
                        mots_probables.append(row)
                else:
                    mots_probables.append(row)

    # si aucun résultat trouvé, rechercher sans filtre consonne/voyelle
    if len(mots_probables) == 0:
        mots_probables = []

        # parcourir chaque ligne du dictionnaire
        for row in ligne_dictionnaire:
            if forme_probable in row[1]:
                mots_probables.append(row)

    mots_probables = sorted(mots_probables, key=lambda row: row[6], reverse=True)

    x = random.randint(1, indice_creativite)

    if x > len(mots_probables):
        x = len(mots_probables)

    mot_choisi = mots_probables[x - 1][0]
    formes_probables = mots_probables[x - 1][1]
    cv_choisi = mots_probables[x - 1][2]
    frequence = mots_probables[x - 1][6]

    # vérifier si le mot choisit et le mot précédent sont compatible
    if cv_choisi[-2][0][-1] == "V" and CV == "C":
        if mots_input[-2][0] == "ce":
            mots_input[-2][0] = mots_input[-2][0].replace("ce", "c'")
        if mots_input[-2][0] == "je":
            mots_input[-2][0] = mots_input[-2][0].replace("je", "j'")
        if mots_input[-2][0] == "ne":
            mots_input[-2][0] = mots_input[-2][0].replace("ne", "n'")
        if mots_input[-2][0] == "se":
            mots_input[-2][0] = mots_input[-2][0].replace("se", "s'")
        if mots_input[-2][0] == "te":
            mots_input[-2][0] = mots_input[-2][0].replace("te", "t'")
        if mots_input[-2][0] == "que":
            mots_input[-2][0] = mots_input[-2][0].replace("que", "qu'")
        if mots_input[-2][0] == "me":
            mots_input[-2][0] = mots_input[-2][0].replace("me", "m'")
        if mots_input[-2][0] == "de":
            mots_input[-2][0] = mots_input[-2][0].replace("de", "d'")
    elif (cv_choisi[-2][0][-1] == "'" or cv_choisi[-2][0][-1] == "C") and CV == "V":
        if mots_input[-2][0] == "c'":
            mots_input[-2][0] = mots_input[-2][0].replace("c'", "ce")
        if mots_input[-2][0] == "j'":
            mots_input[-2][0] = mots_input[-2][0].replace("j'", "je")
        if mots_input[-2][0] == "n'":
            mots_input[-2][0] = mots_input[-2][0].replace("n'", "ne")
        if mots_input[-2][0] == "s'":
            mots_input[-2][0] = mots_input[-2][0].replace("se", "s'")
        if mots_input[-2][0] == "t'":
            mots_input[-2][0] = mots_input[-2][0].replace("t'", "te")
        if mots_input[-2][0] == "qu'":
            mots_input[-2][0] = mots_input[-2][0].replace("qu'", "que")
        if mots_input[-2][0] == "m'":
            mots_input[-2][0] = mots_input[-2][0].replace("m'", "me")
        if mots_input[-2][0] == "d'":
            mots_input[-2][0] = mots_input[-2][0].replace("d'", "de")
        if mots_input[-2][0] == "parce qu'":
            mots_input[-2][0] = mots_input[-2][0].replace("parce qu'", "parce que")

    # supprimer la dernière ligne de la liste pour la remplacer par le mot choisi
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
    
    tableau_resultats = pd.DataFrame(mots_input, columns=['Mot', 'ID', 'ID principal probable', '% ID principal', 'ID précis probable', '% ID précis probable', 'CV', 'Fréquence'])
    tableau_resultats

    with open('logs.txt', "w", encoding='utf-8', newline="") as fichier:
            sauvegarde = csv.writer(fichier, delimiter='|')
            sauvegarde.writerows(mots_input)

    for line in mots_input:
        phrase = " ".join(sublist[0] for sublist in mots_input)

    phrase = phrase.replace(" , ", ", ")
    phrase = phrase.replace("' ", "'")
    phrase = phrase.replace(" .", ".")

    print(phrase)

#----------------------------------------------------------------------------------------------------------------------------------------------------

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = ctk.CTk()
app.geometry("400x240")

def lancement():
    processus_phrases(textbox.get())

textbox = ctk.CTkEntry(master=app)
textbox.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

button = ctk.CTkButton(master=app, text="compléter...", command=lancement)
button.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

app.mainloop()
