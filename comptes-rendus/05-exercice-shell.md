Exercice shell

Lancement du shell depuis le dossier du projet :

```
cd ~\PycharmProjects\django-tutoriel\djangotutorial
python manage.py shell
```

Question 1 : lister toutes les questions avec leurs attributs

`Question.objects.all()` renvoie un ensemble de questions que l'on peut parcourir avec une boucle `for`, pour afficher une question par ligne.

```
>>> for q in Question.objects.all():
...     print(q.id, q.question_text, q.pub_date)
...
1 What's new? 2026-11-16 14:10:14+00:00
2 Quel est ton langage préféré ? 2026-11-20 08:50:32+00:00
3 Quelle saison préfères-tu ? 2026-11-10 17:00:00+00:00
4 Quel sport pratiques-tu ? 2026-11-10 11:00:00+00:00
5 Quel est ton animal préféré ? 2026-11-09 14:57:14+00:00
6 Comment viens-tu en cours ? 2026-11-18 05:00:00+00:00
```

Les dates sont affichées en heure universelle (`+00:00`), comme Django les stocke.

Question 2 : filtrer les questions selon la date de publication

Le double souligné permet de filtrer sur une partie de la date : `__year` (année), `__month` (mois, de 1 à 12), `__day` (jour du mois, de 1 à 31).

```
>>> Question.objects.filter(pub_date__year=2026)
<QuerySet [<Question: What's new?>, <Question: Quel est ton langage préféré ?>, <Question: Quelle saison préfères-tu ?>, <Question: Quel sport pratiques-tu ?>, <Question: Quel est ton animal préféré ?>, <Question: Comment viens-tu en cours ?>]>
>>> Question.objects.filter(pub_date__year=2026, pub_date__month=11, pub_date__day=10)
<QuerySet [<Question: Quelle saison préfères-tu ?>, <Question: Quel sport pratiques-tu ?>]>
```

Toutes les questions ayant été publiées en 2026, le premier filtre les renvoie toutes. Le second, plus précis, ne renvoie que les deux questions publiées le 10 novembre 2026.

Question 3 : la question d'id 2, ses attributs et ses choix

`get(pk=2)` récupère la question dont la clé primaire vaut 2. `q.choice_set.all()` donne ensuite tous ses choix.

```
>>> q = Question.objects.get(pk=2)
>>> print(q.id, q.question_text, q.pub_date)
2 Quel est ton langage préféré ? 2026-11-20 08:50:32+00:00
>>> for c in q.choice_set.all():
...     print(c.id, c.choice_text, c.votes)
...
4 python 2
5 javascript 1
6 java 0
```

Question 4 : chaque question et ses choix

Deux boucles imbriquées : pour chaque question, on parcourt ses choix avec `choice_set.all()`.

```
>>> for q in Question.objects.all():
...     print(q.id, q.question_text, q.pub_date)
...     for c in q.choice_set.all():
...         print("   ", c.id, c.choice_text, c.votes)
...
1 What's new? 2026-11-16 14:10:14+00:00
    1 Not much 5
    2 The sky 1
2 Quel est ton langage préféré ? 2026-11-20 08:50:32+00:00
    4 python 2
    5 javascript 1
    6 java 0
3 Quelle saison préfères-tu ? 2026-11-10 17:00:00+00:00
    7 printemps 3
    8 été 3
    9 hivers 3
4 Quel sport pratiques-tu ? 2026-11-10 11:00:00+00:00
    10 volleyball 6
    11 surf 2
    12 tennis 6
5 Quel est ton animal préféré ? 2026-11-09 14:57:14+00:00
    13 dauphin 0
    14 chien 4
    15 chat 2
6 Comment viens-tu en cours ? 2026-11-18 05:00:00+00:00
    16 voiture 7
    17 bus 0
    18 vélo 1
```

La question 1 n'a que deux choix : le troisième (id 3) a été supprimé lors du tutoriel.

Question 5 : nombre de choix par question

`count()` renvoie le nombre de choix sans les afficher.

```
>>> for q in Question.objects.all():
...     print(q.question_text, ":", q.choice_set.count(), "choix")
...
What's new? : 2 choix
Quel est ton langage préféré ? : 3 choix
Quelle saison préfères-tu ? : 3 choix
Quel sport pratiques-tu ? : 3 choix
Quel est ton animal préféré ? : 3 choix
Comment viens-tu en cours ? : 3 choix
```

Question 7 : tri antéchronologique

`order_by("-pub_date")` trie par date de publication ; le `-` inverse l'ordre (de la plus récente à la plus ancienne).

```
>>> for q in Question.objects.order_by("-pub_date"):
...     print(q.pub_date, q.question_text)
...
2026-11-20 08:50:32+00:00 Quel est ton langage préféré ?
2026-11-18 05:00:00+00:00 Comment viens-tu en cours ?
2026-11-16 14:10:14+00:00 What's new?
2026-11-10 17:00:00+00:00 Quelle saison préfères-tu ?
2026-11-10 11:00:00+00:00 Quel sport pratiques-tu ?
2026-11-09 14:57:14+00:00 Quel est ton animal préféré ?
```

Question 9 : créer une question

```
>>> q = Question(question_text="Quel est ton plat préféré ?", pub_date=timezone.now())
>>> q.save()
>>> print(q.id, q.question_text, q.pub_date)
7 Quel est ton plat préféré ? 2026-11-10 14:03:28.950777+00:00
```

`timezone.now()` donne la date et l'heure actuelles. La question n'est enregistrée dans la base qu'au moment de l'appel à `save()` ; Django lui attribue alors automatiquement l'id 7.


Question 10 : ajouter 3 choix à cette question

```
>>> q.choice_set.create(choice_text="pizza", votes=0)
<Choice: pizza>
>>> q.choice_set.create(choice_text="sushi", votes=0)
<Choice: sushi>
>>> q.choice_set.create(choice_text="couscous", votes=0)
<Choice: couscous>
>>> for c in q.choice_set.all():
...     print(c.id, c.choice_text, c.votes)
...
21 pizza 0
22 sushi 0
23 couscous 0
```

`choice_set.create()` crée le choix, le rattache à la question `q` et l'enregistre en une seule opération.

Question 11 : lister les questions publiées récemment

Une question est considérée comme récente si elle a été publiée dans les dernières 24 heures, comme dans la méthode `was_published_recently()` du tutoriel.

```
>>> import datetime
>>> maintenant = timezone.now()
>>> Question.objects.filter(pub_date__gte=maintenant - datetime.timedelta(days=1), pub_date__lte=maintenant)
<QuerySet [<Question: Quel sport pratiques-tu ?>, <Question: Quel est ton animal préféré ?>, <Question: Quel est ton plat préféré ?>]>
```

- `datetime.timedelta(days=1)` représente une durée d'un jour ;
- `__gte` signifie « supérieur ou égal », `__lte` « inférieur ou égal ».

La condition `pub_date__lte=maintenant` exclut les questions dont la date de publication est dans le futur. Sans elle, la question « Quelle saison préfères-tu ? » (datée du 10 novembre à 17h00 UTC, donc pas encore publiée au moment de la requête) aurait été comptée comme récente. La méthode `was_published_recently()` du tutoriel présente ce défaut, corrigé dans la 5e partie.

Petite remarque : 
Mes nouveaux choix ont les ids 21 à 23 et non 19 à 21 car deux choix ont été créés puis supprimés à un moment (dans l’admin). Django ne réutilise jamais un id supprimé.