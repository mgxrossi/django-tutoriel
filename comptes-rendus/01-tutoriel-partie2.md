# Écriture de notre première application Django 2e partie](https://docs.djangoproject.com/fr/5.2/intro/tutorial02/)

Objectif

Donner une base de données à l'application de sondages :

- configurer le projet (langue, fuseau horaire, base de données) ;
- décrire les données à stocker sous forme de **modèles** (`Question` et `Choice`) ;
- créer les tables correspondantes grâce aux **migrations** ;
- manipuler les données avec le **shell Django** ;
- découvrir le **site d'administration** généré automatiquement par Django.

Toutes les commandes `python manage.py ...` sont lancées depuis le dossier `djangotutorial`, environnement virtuel activé.


1.Configuration du projet

Modifications dans `mysite/settings.py`, conformément au sujet :

LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'Europe/Paris'

La base de données utilisée est celle par défaut, **SQLite** (réglage `DATABASES`). Elle tient dans un simple fichier, `db.sqlite3`, et ne nécessite aucune installation supplémentaire.


2. Création des tables de base

```
python manage.py migrate
```

Les applications fournies avec Django et listées dans `INSTALLED_APPS` (administration, authentification, sessions…) ont besoin de tables. Cette commande les crée et génère le fichier `db.sqlite3`.

Tables obtenues (observées avec DB Browser for SQLite) :

| Table | Contenu |

| `auth_user` | Les comptes utilisateurs |
| `auth_group` | Les groupes d'utilisateurs |
| `auth_permission` | La liste des droits possibles |
| `auth_user_groups`, `auth_user_user_permissions`, `auth_group_permissions` | Les liens entre utilisateurs, groupes et droits |
| `django_migrations` | L'historique des migrations appliquées |
| `django_session` | Les sessions (maintien de la connexion) |
| `django_admin_log` | L'historique des actions faites dans l'administration |
| `django_content_type` | La liste des modèles du projet (usage interne) |
| `sqlite_sequence` | Table interne à SQLite (dernier `id` attribué dans chaque table) |

Règle de nommage : Django nomme chaque table `<application>_<modèle en minuscules>`. Par exemple, le modèle `User` de l'application `auth` donne la table `auth_user`.


3. Création des modèles

Un modèle est une classe Python qui décrit un type de données à stocker. Chaque attribut de la classe devient une colonne de la table.


| Élément | Signification |

| `CharField(max_length=200)` | Texte court, 200 caractères maximum |
| `DateTimeField("date published")` | Date et heure ; le texte est un nom plus lisible pour le champ |
| `IntegerField(default=0)` | Nombre entier, valant 0 par défaut |
| `ForeignKey(Question, on_delete=models.CASCADE)` | Lien vers une question : chaque choix appartient à une seule question. Si la question est supprimée, ses choix le sont aussi |
| `__str__` | Définit l'affichage d'un objet (son texte au lieu de « Question object (1) ») |
| `was_published_recently` | Méthode personnalisée : indique si la question a été publiée il y a moins d'un jour |


4. Activation des modèles

Pour que le projet prenne en compte l'application `polls`, elle est ajoutée au réglage `INSTALLED_APPS` de `mysite/settings.py` :

INSTALLED_APPS = [
    "polls.apps.PollsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

`polls.apps.PollsConfig` désigne la classe de configuration de l'application, située dans `polls/apps.py`.

Création puis application de la migration :

python manage.py makemigrations polls
python manage.py sqlmigrate polls 0001
python manage.py migrate


| Commande | Rôle |

| `makemigrations polls` | Compare les modèles à la base et écrit les changements dans un fichier de migration (`polls/migrations/0001_initial.py`) |
| `sqlmigrate polls 0001` | Affiche le code SQL correspondant, sans rien exécuter (pour information) |
| `migrate` | Applique la migration : les tables sont réellement créées |

Deux nouvelles tables apparaissent : `polls_question` et `polls_choice`.

Correspondance entre modèles et colonnes :

| Table | Colonnes |

| `polls_question` | `id` (ajouté automatiquement, clé primaire), `question_text`, `pub_date` |
| `polls_choice` | `id`, `choice_text`, `votes`, `question_id` |

La colonne `question_id` est produite par la `ForeignKey` : elle contient l'`id` de la question à laquelle le choix appartient. C'est elle qui relie les deux tables.


Démarche à suivre à chaque modification des modèles :

1. modifier `models.py` ;
2. `python manage.py makemigrations` ;
3. `python manage.py migrate`.

Les fichiers de migration sont versionnés sur GitHub : ils permettent de recréer la même structure de base de données sur un autre ordinateur.

5. Manipulation des données avec le shell Django

python manage.py shell

Le shell Django est une console Python reliée au projet : on peut y créer, rechercher, modifier et supprimer des données. Les modèles y sont importés automatiquement.


Créer et modifier une question

```python
>>> Question.objects.all()
<QuerySet []>
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())
>>> q.save()
>>> q.id
1
>>> q.question_text = "What's up?"
>>> q.save()
>>> Question.objects.all()
<QuerySet [<Question: What's up?>]>
```

- `objects.all()` renvoie toutes les questions.
- `save()` enregistre l'objet dans la base ; sans cet appel, rien n'est stocké.
- Django attribue automatiquement l'`id`.


Rechercher des questions

```python
>>> Question.objects.filter(id=1)
<QuerySet [<Question: What's up?>]>
>>> Question.objects.filter(question_text__startswith="What")
<QuerySet [<Question: What's up?>]>
>>> current_year = timezone.now().year
>>> Question.objects.get(pub_date__year=current_year)
<Question: What's up?>
>>> Question.objects.get(id=2)
DoesNotExist: Question matching query does not exist.
>>> Question.objects.get(pk=1)
<Question: What's up?>
>>> q.was_published_recently()
True
```

| Méthode | Résultat |

| `filter(...)` | Une liste (`QuerySet`) d'objets correspondant au critère, éventuellement vide |
| `get(...)` | Un seul objet ; provoque une erreur `DoesNotExist` s'il n'existe pas |
| `pk` | Raccourci pour la clé primaire (ici `id`) |


Ajouter et parcourir des choix

```python
>>> q.choice_set.all()
<QuerySet []>
>>> q.choice_set.create(choice_text="Not much", votes=0)
<Choice: Not much>
>>> q.choice_set.create(choice_text="The sky", votes=0)
<Choice: The sky>
>>> c = q.choice_set.create(choice_text="Just hacking again", votes=0)
>>> c.question
<Question: What's up?>
>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> q.choice_set.count()
3
```

`choice_set` représente l'ensemble des choix d'une question. Il est créé automatiquement par Django grâce à la `ForeignKey` du modèle `Choice`. La relation fonctionne dans les deux sens : `c.question` donne la question d'un choix, `q.choice_set` donne les choix d'une question.


La notation double-underscore

```python
>>> Choice.objects.filter(question__pub_date__year=current_year)
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> c = q.choice_set.filter(choice_text__startswith="Just hacking")
>>> c.delete()
```

Le double souligné `__` a deux usages :

- préciser une recherche sur un champ : `choice_text__startswith="Just hacking"` signifie « dont le texte commence par Just hacking » (voir Recherches dans les champs) ;
- traverser une relation : `question__pub_date__year` signifie « l'année de la date de publication de la question liée au choix » (voir Recherches traversant les relations).


Vérification dans DB Browser for SQLite

Après `exit()`, l'onglet Parcourir les données montre une ligne dans `polls_question` (« What's up? ») et deux lignes dans `polls_choice`, toutes deux avec `question_id = 1`. Les opérations du shell ont bien été enregistrées dans la base.


6. Le site d'administration

Le site d'administration est un espace réservé aux gestionnaires du site, généré automatiquement par Django, qui permet d'ajouter, modifier et supprimer des données via des formulaires.


Création d'un super-utilisateur
```
python manage.py createsuperuser
```

Saisie d'un nom d'utilisateur, d'une adresse e-mail et d'un mot de passe (non affiché lors de la frappe). Ce compte a tous les droits sur l'administration.


Accès à l'administration

```
python manage.py runserver
```

Adresse : http://127.0.0.1:8000/admin/. La page de connexion est en français grâce au réglage `LANGUAGE_CODE`. Après connexion, seules les rubriques *Groupes* et *Utilisateurs* (application `auth`) sont visibles.


Inscription du modèle `Question`

Fichier `polls/admin.py` :

```python
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```

`admin.site.register(Question)` indique à Django que le modèle `Question` doit être gérable depuis l'administration. Après rechargement de la page, la rubrique *Polls > Questions* apparaît.


Exploration

- La liste des questions affiche « What's up? », créée dans le shell.
- Le formulaire de modification est généré automatiquement à partir du modèle : un champ texte pour `question_text`, un calendrier et une horloge pour `pub_date`.
- Le bouton Historique liste les modifications effectuées sur l'objet, avec la date, l'heure et l'utilisateur.

Le shell, l'administration et DB Browser for SQLite sont trois manières d'accéder à la même base de données : une question ajoutée dans l'administration apparaît aussi dans la table `polls_question`.


7. Problèmes rencontrés

| Problème | Cause | Solution |

| `can't open file '...\django-tutoriel\manage.py'` | Commande lancée depuis la racine du dépôt au lieu du dossier du projet | Se placer dans `djangotutorial` (`cd djangotutorial`) : les commandes Git se lancent depuis `django-tutoriel`, les commandes Django depuis `djangotutorial` |


8. Sauvegarde sur GitHub

```
git add .
git commit -m "Tutoriel partie 2 : modèles, migrations et site d'administration"
git push
```

Le fichier `db.sqlite3` est exclu du dépôt par le `.gitignore` ; les fichiers de migration, eux, sont bien versionnés.


Bilan

- Projet configuré en français et à l'heure de Paris.
- Modèles `Question` et `Choice` créés, reliés par une clé étrangère, et traduits en tables par les migrations.
- Données créées, recherchées, modifiées et supprimées avec le shell Django.
- Site d'administration opérationnel, avec le modèle `Question` inscrit.


