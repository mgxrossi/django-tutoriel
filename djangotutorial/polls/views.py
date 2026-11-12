from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Choice, Question
from django.shortcuts import get_object_or_404, render
from django.urls import reverse



def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    #"latest_question_list" est le nom que le gabarit utilisera
    #à droite du = c'est la variable Python qui contient les données
    template = loader.get_template("polls/index.html")
    context = {"latest_question_list": latest_question_list}
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    #va chercher la question qui a ce numéro, ou affiche page introuvable
    #question_id, c’est le numéro pris dans l’adresse (le 1 de /polls/1/)
    return render(request, "polls/detail.html", {"question": question})
    #donne cette question à la feuille detail.html, avec l’étiquette question


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


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