Entrainement du modèle 'brouhaha'

Assurez-vous de placer le fichier 'dictionnaire.txt' à la même racine que votre répertoire d'entrainement.

1) Traitement des données de text brut
	Input : 'phrases.txt'
	Output : 'mots.txt'

	Placez un fichier texte nommé 'phrases.txt' dans la même racine que votre répertoire d'entrainement, ce fichier doit contenir une phrase par ligne.
	Le programme 1) va identifier tous les mots et/ou expressions présentes à la fois dans le fichier 'phrases.txt' et dans le fichier 'dictionnaire.txt'.
	Chaque mot ou expression sera identiable par le symbole "|".
	Vous obtiendrez alors un fichier 'mots.txt' composé de l'étude de l'ensemble du fichier 'phrases.txt'.

2) Évaluation et attribution des formes probables
	Input : 'mots.txt'
	Output : 'silence.txt'
	
	Sur la base du fichier 'mots.txt', ce second programme va évaluer la forme la plus probable de chaque mot employé dans chaque phrase.
	Par exemple :
	- dans la phrase "ce n'est pas", le programme va identifier que "ce" est un pronom, "n'" un adverbe, "est" un verbe et "pas" un adverbe ;
	- dans la phrase "c'est un pas", le programme va identifier que "c'" est un pronom, "est" un verbe et "pas" un nom.
	Ce programme finalise l'entrainement du modèle et permet de générer le fichier 'silence.txt'.
