from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"), #une vue générique est une classe (un « modèle de vue »), pas une fonction
                                                             #.as_view() la transforme en vue utilisable par urls.py. Toujours l’ajouter
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("all/", views.all_polls, name="all"),
    #"all/" : l’adresse, qui donne /polls/all/ (le polls/ vient de mysite/urls.py
    #views.all_polls : la fonction qui s’en occupe
    #name="all" : son nom, pour faire des liens avec % url 'polls:all' %
    path("<int:question_id>/frequency/", views.frequency, name="frequency"),
    #un numéro dans l’adresse, et c’est une fonction, donc on garde le nom question_id
]