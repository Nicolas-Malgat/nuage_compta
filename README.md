<p  align="center">
<h1  align="center">Nuage Compta</h3>
</p>

## Sommaire

*  [Contexte du projet](#contexte-du-projet)

*  [Commencer](#commencer)

*  [Utilisation](#utilisation)

*  [Auteurs](#auteurs)


## Contexte du projet

La société Nuage est une société éditrice d'un logiciel spécialisé dans la gestion de la comptabilité pour les entreprises de toutes tailles : Nuage Compta.

Suite a un sondage auprès de ses clients sur les principales améliorations qu'ils souhaitaient voir intégrer dans le logiciel, la société souhaite développer un modèle de reconnaissance de texte appliqué aux factures de ses clients. Le but de ce modèle serait les aider dans la saisie comptable des pièces de type facture.

La société ne possède pas les ressources nécessaires pour développer un tel module et vous sollicite afin de l'aider à créer ce système.

## Commencer

Pour avoir une copie locale et lancer le programme, suivez ces étapes.

### Installation

1. Cloner le répertoire
```git
git clone https://github.com/diem-ai/Immothep.git
```
2. Créer un environnement conda avec
```bash
conda create --name <env> --file package-list.txt
```
## Utilisation

- Lancer [CNN.ipynb](https://github.com/Nicolas-Malgat/nuage_compta/blob/main/CNN.ipynb)
	- Ce notebook va générer le modèle ( [1000_CNN.h5](https://github.com/Nicolas-Malgat/nuage_compta/blob/main/1000_CNN.h5) ) pour l'évaluation des images.

- Lancer [OpenCV.ipynb](https://github.com/Nicolas-Malgat/nuage_compta/blob/main/OpenCV.ipynb)
	- Ce notebook charge une image dans la première cellule,
	   puis se découpe en deux parties:
		- La première donne une prédiction sur l'image 
		- La seconde permet d'ajuster si nécessaire les filtres sur l'image

> Le notebook [test_lettre_individuel.ipynb](https://github.com/Nicolas-Malgat/nuage_compta/blob/main/test_lettre_individuel.ipynb "test_lettre_individuel.ipynb") permet de dessiner des lettres ou chiffres afin de les soumettre au modèle de manière interactive.

## Auteurs

Farida Olivier
Nicolas Malgat
