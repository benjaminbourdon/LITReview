# LitReview

Ce programme utilise le framework Django.
Il propose un site minimal de critiques partagées d'oeuvre littéraire.

## Pré-requis

- Python 3.x (développé avec Python 3.11.3)
- Django > 4.2
- Pillow (pour la gestion des images)

L'ensemble des dépendances sont consultables dans le fichier *requirements.txt*

## Installation

1. Clonez ce dépôt sur votre machine locale.
``` git clone https://github.com/benjaminbourdon/LITReview.git ```
2. Accédez au répertoire du projet. Par exemple, ```cd LITReview```
3. Créez un environnement virtuel.  
La documentation recommande *pipenv*. 
Si *pipenv* est déjà installé sur votre système : 
``` pipenv install ```
Alternativement, avec *venv* :
``` python3 -m venv env ```
4. Activez l'environnement virtuel :
    + Avec *pipenv* : ```pipenv shell```
    + Avec *venv* : 
        + Sur macOS et Linux : ```source env/bin/activate```
        + Sur Windows avec PowerShell : ```env\Scripts\Activate.ps1```
5. Si vous avez choisi *venv*, installez les dépendances manuellement : 
```pip install -r requirements.txt```  
Avec pipenv, les dépendances ont automatiquement été installées lors de la création de l'environnement virtuel. Vous pouvez le vérifier avec :
```pipenv graph```
6. Effectuez les migrations de la base de données.  
Le dépôt inclut un fichier *db.sqlite3* à des fins de test.
Il est recommandé de supprimer ce fichier et de créer la base de données (vide) avec : 
```python manage.py migrate```
7. Lancez le serveur de développement : ```python manage.py runserver```

## Utilisation 

1. Executez le serveur de développement : ```python manage.py runserver```
2. Accédez à l'URL <http://localhost:8000/> dans votre navigateur
3. Si vous avez gardé la base de données de test, vous pouvez directement vous connecter avec un des comptes existants : 
    - ArticLapin, AuroreAlchimie, BenjaminBabar, GabinÉtoiles, IllaMystère, JulesEnigmes, LéoSable, MaxHorloger, RaphyChat, ViolettePlume ou ÉliseLivre  
    Le mot de passe est toujours [XY]-OC2023 avec [XY] : les deux initiales (lettres en capitales, sans accent) du nom de l'utilisateurices.  
    Par exemple, identifiant : *ArticLapin* , mot de passe : *AL-OC2023*  
    - En cas de nouvelle base de données, créez un nouveau super-utilisateur avec la commande :
    ```python manage.py createsuperuser```

4. Pour accéder à l'espace admin, vous devez vous rendre à l'adresse : <http://localhost:8000/admin>  
Avec les données de test, l'utilisateur à utiliser est *BenjaminB* pour y accéder.

## Structure du projet

Le projet suit la structure standard du framework Django.

- **LITReview** : répertoire racine du projet Django
    - **config/** : contient les fichiers du configuration principaux
    - **review/** : répertoire contenant l'application au sens de Django
    - **media/** : répertoire où sont stockés les médias, notamment les images
    - **static/** : répertoire pour les fichiers statiques (CSS, etc.)
    - **templates/** : répertoires pour les templates HTML non liés à une application spécifiques
    - **core_views.py** : *views* utilisés par le projets, non liés à un projet spécifique
    - **manage.py** : point d'entrée pour les commandes de gestion Django