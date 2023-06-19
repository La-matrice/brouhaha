<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://age-verify.crucialcommerceapps.com/app/img/logo/Brouhaha%20Brewery%20Logo%20White_1620698403.png">
 <source media="(prefers-color-scheme: light)" srcset="https://cdn.shopify.com/s/files/1/0481/4163/1647/files/Brouhaha-2021-logo-Final.png?v=1631767372">
 <img alt="YOUR-ALT-TEXT" src="https://cdn.shopify.com/s/files/1/0481/4163/1647/files/Brouhaha-2021-logo-Final.png?v=1631767372">
</picture>

#  *un programme capable de générer des phrases aléatoires et grammaticalement correctes...*


> ## Dictionnaire en français
Le premier élément de ce projet est un fichier texte composé de l'ensemble des mots français ainsi que de leurs caractéristiques.
Ce fichier a été formé sur la base de plusieurs sources dont certaines sont disponibles en ligne, comme par exemple le [projet OpenLexicon](http://www.lexique.org/ "www.lexique.org").
L'objectif de ce dictionnaire est d'être en mesure d'identifier la ou les formes grammaticales, le domaine et l'occurence de chaque mot.
La description des différents tags utilisés est disponible **ICI**.

> ## Phrases en français
- Pour compléter la richesse du dictionnaire et permettre une évaluation et une prédiction cohérentes, un second fichier texte est utilisé.
Celui-ci contient une liste de phrases en français, issues de 7 livres distincts. Chaque ligne dispose d'une seule phrase et tous les mots sont séparés par le symbole "|" (dans le but d'accélérer le processus de recherche et de manipulation de caractères).

> ## Entrainement du modèle
- 

> ## Utilisation du modèle entrainé
- Le programme fonctionne de manière très simple.
- Tout d'abord, l'utilisateur saisit le début d'une phrase d'au moins deux mots.
S'exécute alors la première phase du programme. Celle-ci consiste à identifier les mots saisis par l'utilisateur et d'en relever leur caractéristiques à l'aide de la base de données 'Dictionnaire.txt'.
Une fois tous les mots identifiés, le résultat est enregistré sous forme de tableau dans un fichier texte.
- La deuxième phase du programme permet de déterminer la forme la plus probables de chaque mot préalablement identifiés.
Si un mot possède plusieurs formes probables (comme par exemple le mot 'pas' qui est à la fois un nom et un adverbe), le programme évalue la forme la plus probable en calculant l'occurence de chaque mot dans le fichier 'Mots.txt' et ce, par rapport à sa position dans la phrase saisit par l'utilisateur.
- La troisième phase est dédiée à la prédiction du mot probable suivant.


> ##  Éléments téléchargeables

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
