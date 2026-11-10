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