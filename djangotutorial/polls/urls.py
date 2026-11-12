from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"), #une vue générique est une classe (un « modèle de vue »), pas une fonction
                                                             #.as_view() la transforme en vue utilisable par urls.py. Toujours l’ajouter
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]