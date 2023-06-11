Ce projet consiste à développer un programme Python capable de générer des phrases grammaticalement correctes et de manière aléatoire.
Pour y parvenir, le programme évalue les suites de mots les plus probables en utilisant deux datasets:
- une base de données de phrases en français, toutes extraites de 7 livres distincts
- et un dictionnaire, qui permet d'identifier la ou les formes grammaticales, le domaine et l'occurence (dans les phrases) de chaque mot.

Voici les principales étapes de ce projet :

1) Dictionnaire en français
- La première étape consiste à former un dictionnaire composés de l'ensemble des mots du dictionnaire ainsi que de leurs caractéristiques.
Pour cela plusieurs sources sont disponibles en ligne, comme par exemple le projet OpenLexicon (http://www.lexique.org/).
Ce dictionnaire, dont le téléchargement est expliqué plus bas, se présente sous la forme d'un fichier texte et identifie un mot par ligne et un type de caractéristique par colonne (les colonnes sont séparées par le symbole "|").

2) Phrases en français
- Pour compléter la richesse du dictionnaire et permettre une évaluation cohérente, un second fichier texte est utilisé.
Celui-ci contient une liste de phrases en français, issues de livres. Chaque ligne dispose d'une seule phrase et tous les mots sont séparés par le symbole "|" (dans le but d'accélérer le processus de recherche et de manipulation de caractères).

3) Programme
- Le programme fonctionne de manière très simple.
- Tout d'abord, l'utilisateur saisit le début d'une phrase d'au moins deux mots.
S'exécute alors la première phase du programme. Celle-ci consiste à identifier les mots saisis par l'utilisateur et d'en relever leur caractéristiques à l'aide de la base de données 'Dictionnaire.txt'.
Une fois tous les mots identifiés, le résultat est enregistré sous forme de tableau dans un fichier texte.
- La deuxième phase du programme permet de déterminer la forme la plus probables de chaque mot préalablement identifiés.
Si un mot possède plusieurs formes probables (comme par exemple le mot 'pas' qui est à la fois un nom et un adverbe), le programme évalue la forme la plus probable en calculant l'occurence de chaque mot dans le fichier 'Mots.txt' et ce, par rapport à sa position dans la phrase saisit par l'utilisateur.
- La troisième phase est dédiée à la prédiction du mot probable suivant.


Les éléments téléchargeables sont décrits ci-dessous.

'datas.zip' composé de fichiers au format txt utilisés pour l'entrainement du programme :
- 'Dictionnaire.txt' contenant plus de 435 000 mots en français et leurs caractéristiques grammaticales
- 'Mots.txt' contenant plus de 33 000 phrases en français et dont tous les mots sont séparés par le symbole '|'
- 'Formes.txt' qui correspond au fichiers 'Mots.txt' mais pour lequel les mots ont été remplacés par leurs caractéristiques présentes dans le fichier 'Dictionnaire.txt'

'preparation_datas.zip' composé de deux programmes Python et du résultat de leur exécution :
- 'A_identification_phrases_vers_mots.py'
- 'B_conversion_mots_vers_formes.py'
- 'dictionnaire.txt'
- 'dictionnaire_formes.txt'
- 'phrases.txt'
- 'resultat_conversion.txt'
- 'resultat_identification.txt'
