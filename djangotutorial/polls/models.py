import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def get_choices(self):
        choices = self.choice_set.all()  #prends tous les choix de cette question » (self = la question concernée)
        total = sum(choice.votes for choice in choices) #additionne les votes de tous les choix
        result = []   #prépare une liste vide
        for choice in choices:  #pour chaque choix
            if total > 0:  #si quelqu’un a voté, calcule le pourcentage
                proportion = round(choice.votes / total * 100, 2)  #round, arrondi à 2 chiffres après la virgule
            else:
                proportion = 0   #sinon, 0 % » (on ne peut pas diviser par zéro)
            result.append((choice, choice.votes, proportion))   #ajoute à la liste un paquet de 3 infos (tuple) : le choix, ses votes, son pourcentage
        return result    #La méthode renvoie une liste de tuples, par exemple : [(python, 2, 66.67), (javascript, 1, 33.33), (java, 0, 0.0)]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text