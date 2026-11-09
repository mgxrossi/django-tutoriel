# Compte-rendu 00 – Installation de l'environnement de travail

## Objectif

Mettre en place l'environnement nécessaire au module Django :

- un environnement virtuel Python dédié au module ;
- Django en version **5.2.18** (version imposée par le sujet) ;
- le projet du tutoriel officiel (`mysite`, dans le dossier `djangotutorial`) ;
- un dépôt GitHub pour héberger le code et les comptes-rendus.

Système utilisé : Windows, terminal PowerShell (intégré à PyCharm).

## Organisation des dossiers

```
PycharmProjects/
└── django-tutoriel/        ← dossier du module (dépôt GitHub)
    ├── .venv/              ← environnement virtuel (non versionné)
    ├── djangotutorial/     ← projet Django du tutoriel
    │   ├── manage.py
    │   └── mysite/         ← réglages du projet (settings.py, urls.py…)
    ├── comptes-rendus/     ← comptes-rendus au format Markdown
    ├── .gitignore
    └── requirements.txt
```

Les comptes-rendus sont placés dans un répertoire séparé de celui du projet Django, comme demandé dans le sujet.

## 1. Création de l'environnement virtuel et installation de Django

| Commande | Rôle |
|---|---|
| `cd ~\PycharmProjects` | Se placer dans le dossier PycharmProjects |
| `mkdir django-tutoriel` | Créer le dossier du module |
| `cd django-tutoriel` | Entrer dans ce dossier |
| `py -m venv .venv` | Créer l'environnement virtuel dans le sous-dossier `.venv` |
| `.venv\Scripts\activate` | Activer l'environnement (`(.venv)` apparaît en début de ligne) |
| `python -m pip install Django==5.2.18` | Installer la version de Django demandée |
| `python -m django --version` | Vérifier l'installation (affiche `5.2.18`) |

Un **environnement virtuel** est une installation de Python propre au projet : les paquets installés (ici Django) n'affectent pas le reste de l'ordinateur, et chaque projet peut utiliser ses propres versions.

## 2. Création du projet Django

Conformément à la 1re partie du tutoriel officiel :

| Commande | Rôle |
|---|---|
| `mkdir djangotutorial` | Créer le dossier qui contiendra le projet |
| `django-admin startproject mysite djangotutorial` | Générer le projet `mysite` dans `djangotutorial` |
| `mkdir comptes-rendus` | Créer le dossier des comptes-rendus |

## 3. Lancement du serveur de développement

| Commande | Rôle |
|---|---|
| `cd djangotutorial` | Aller dans le dossier contenant `manage.py` |
| `python manage.py runserver` | Lancer le serveur de développement |
| `Ctrl + C` | Arrêter le serveur |

Le site est alors visible à l'adresse http://127.0.0.1:8000 (page « Félicitations ! » avec une fusée).

## 4. Problème rencontré et solution

Au premier lancement du serveur, l'erreur suivante est apparue :

```
ModuleNotFoundError: No module named 'django'
```

**Cause :** l'environnement virtuel n'était pas activé dans le terminal. Python utilisait donc l'installation globale de l'ordinateur, dans laquelle Django n'est pas installé. On le repère car l'invite de commande ne commence pas par `(.venv)`.

**Solution :** activer l'environnement depuis le dossier `djangotutorial` (le dossier `.venv` est un niveau au-dessus) :

```
..\.venv\Scripts\activate
```

Si PowerShell bloque l'exécution du script d'activation, il faut l'autoriser une fois pour l'utilisateur courant :

```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Pour éviter le problème à l'avenir, l'interpréteur du `.venv` a été configuré dans PyCharm (*Settings > Project > Python Interpreter*) : le terminal de PyCharm active alors l'environnement automatiquement.

## 5. Mise en place du dépôt GitHub

### Fichiers préparés

- `.gitignore` : exclut du dépôt l'environnement virtuel (`.venv/`), les fichiers compilés (`__pycache__/`, `*.pyc`), la base de données locale (`db.sqlite3`) et la configuration de PyCharm (`.idea/`).
- `requirements.txt` : liste des paquets installés, pour pouvoir recréer l'environnement. Généré avec :

```
python -m pip freeze | Out-File -Encoding utf8 requirements.txt
```

### Commandes

| Commande | Rôle |
|---|---|
| `git config --global user.name "…"` | Indiquer son nom à Git (une seule fois par ordinateur) |
| `git config --global user.email "…"` | Indiquer son e-mail (celui du compte GitHub) |
| `git init` | Créer le dépôt local |
| `git add .` | Sélectionner tous les fichiers pour le prochain enregistrement |
| `git status` | Vérifier la sélection (`.venv` ne doit pas apparaître) |
| `git commit -m "message"` | Enregistrer une version avec un message descriptif |
| `git branch -M main` | Nommer la branche principale `main` |
| `git remote add origin https://github.com/<pseudo>/django-tutoriel.git` | Relier le dépôt local au dépôt GitHub |
| `git push -u origin main` | Envoyer le code sur GitHub (première fois) |

### Routine après chaque étape

```
git add .
git commit -m "Description de ce qui a été fait"
git push
```

## Récapitulatif : début de chaque séance de travail

```
cd ~\PycharmProjects\django-tutoriel
.venv\Scripts\activate
cd djangotutorial
python manage.py runserver
```
