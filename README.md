Ce projet consiste à développer un programme Python capable de générer des phrases grammaticalement correctes et de manière aléatoire.
Pour y parvenir, le programme évalue les suites de mots les plus probables en utilisant deux datasets:
- une base de données de phrases en français, toutes extraites de 7 livres distincts
- et un dictionnaire, qui permet d'identifier la ou les formes grammaticales, le domaine et l'occurence (dans les phrases) de chaque mot.

Voici les principales étapes de ce projet :

1) Dictionnaire en français
La première étape consiste à former un dictionnaire composés de l'ensemble des mots du dictionnaire ainsi que de leurs caractéristiques.
Pour cela plusieurs sources sont disponibles en ligne, comme par exemple le projet OpenLexicon (http://www.lexique.org/).
Ce dictionnaire, dont le téléchargement est expliqué plus bas, se présente sous la forme d'un fichier texte et identifie un mot par ligne et un type de caractéristique par colonne (les colonnes sont séparées par le symbole "|").

2) Phrases en français
Pour compléter la richesse du dictionnaire et être en mesure d'éva

4) Préparation des données
La première étape consiste à 





Les éléments téléchargeables sont décrits ci-dessous.

'datas.zip' composé de fichiers au format txt utilisés pour l'entrainement du programme :
- 'Dictionnaire.txt' contenant plus de 435 000 mots en français et leurs caractéristiques grammaticales
- 'Mots.txt' contenant plus de 33 000 phrases en français et dont tous les mots sont séparés par le symbole '|'
- 'Formes.txt' qui correspond au fichiers 'Mots.txt' mais pour lequel les mots ont été remplacés par leurs caractéristiques présentes dans le fichier 'Dictionnaire.txt'
