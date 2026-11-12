from django.http import HttpResponse
from django.template import loader
from .models import Question
from django.shortcuts import render


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
    return HttpResponse("You're voting on question %s." % question_id)