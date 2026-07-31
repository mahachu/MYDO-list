##  Installation & Démarrage

### 1. Cloner le projet

```bash
git clone ...
```

### 2. Créer un environnement virtuel

```bash
python3 -m venv venv
```

### 3. Activer l'environnement

```bash
source venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

### 6. Lancer le serveur

```bash
python manage.py runserver
```