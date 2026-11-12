from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Choice, Question
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    #avec ListView django écris le plateau et choisit l’étiquette tout seul, avec une règle fixe : nom du modèle en minuscules + _list. Pour le modèle Question, ça donne question_list
    #pb ma feuille cherche latest_question_list, Django a écrit question_list donc on mets l’étiquette latest_question_list sur le plateau
    #feuille index.html cherche l’étiquette latest_question_list : html % for question in latest_question_list %

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]  #Voici quelles questions lister : les 5 plus récentes


class DetailView(generic.DetailView):
    model = Question   #il s'agit de questions
    template_name = "polls/detail.html"  #Utilise cette feuille à trous


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    #« Je trouve la question ou page introuvable
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        # Je regarde quel choix a été coché » : request.POST["choice"] = le numéro envoyé par le formulaire (le 4 de choice=4)
    except (KeyError, Choice.DoesNotExist):
    # Si rien n’est coché : je réaffiche le formulaire avec le message « You didn’t select a choice
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F("votes") + 1
        #F("votes") + 1 au lieu de votes + 1 : ça demande à la base elle-même d’ajouter 1 au cas ou deux personnes votent pile en même temps.
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    # Sinon » (else) : j’ajoute +1 vote, j’enregistre, et j’envoie le visiteur vers la page des résultats
    #Le renvoi vers les résultats (HttpResponseRedirect) : sans lui, si le visiteur actualise la page, son vote serait compté deux fois.
    # On le renvoie donc ailleurs juste après le vote


def all_polls(request):
    questions = Question.objects.order_by("id")
    #va chercher toutes les questions, rangées par numéro
    return render(request, "polls/all.html", {"questions": questions})
    #donne-les à la feuille all.html, avec l’étiquette questions