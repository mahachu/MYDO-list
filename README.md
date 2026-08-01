# MYDO list

Une application web de gestion de tâches (to-do list), développée avec Django, permettant de créer, suivre et organiser ses tâches quotidiennes avec des dates d'échéance.

## Objectif du projet

MYDO list a été conçu comme projet d'apprentissage de Django, dans le but de mettre en pratique les concepts fondamentaux du framework : modèles, vues, templates, formulaires, ainsi que des interactions dynamiques côté client avec AJAX (recherche et filtrage en temps réel, sans rechargement de page).

## Fonctionnalités

- **Créer une tâche** avec un titre, une description et une date d'échéance
- **Modifier** une tâche existante
- **Supprimer** une tâche, avec une page de confirmation dédiée
- **Marquer une tâche comme terminée** en un clic, directement depuis la liste (sans recharger la page)
- **Rechercher** une tâche par titre ou description, avec mise à jour instantanée des résultats
- **Filtrer** les tâches par statut : Toutes / À faire / Terminées
- **Suivi automatique du statut** d'une tâche :
  - *À faire* : tâche non terminée, échéance non dépassée
  - *En retard* : tâche non terminée, dont la date d'échéance est passée
  - *Terminée* : tâche marquée comme achevée, avec sa date de complétion enregistrée
- **Interface responsive**, adaptée aux écrans mobiles, tablettes et ordinateurs

## Stack technique

- **Backend** : Django (Python)
- **Frontend** : HTML, CSS, JavaScript (vanilla, sans framework)
- **Base de données** : SQLite (par défaut en développement)

## Installation & Démarrage

### 1. Cloner le projet

​```bash
git clone https://github.com/mahachu/MYDO-list.git
cd MYDO-list
​```

### 2. Créer un environnement virtuel

​```bash
python3 -m venv venv
​```

### 3. Activer l'environnement

Sur Mac/Linux :
​```bash
source venv/bin/activate
​```

Sur Windows :
​```bash
venv\Scripts\activate
​```

### 4. Installer les dépendances

​```bash
pip install -r requirements.txt
​```

### 5. Appliquer les migrations

​```bash
python manage.py migrate
​```

### 6. Lancer le serveur

​```bash
python manage.py runserver
​```

### 7. Ouvrir l'application

Ouvre ton navigateur à l'adresse : [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## À venir
- Authentification des utilisateurs (inscription, connexion, déconnexion)
- Chaque utilisateur pourra créer et gérer sa propre liste de tâches, indépendante des autres