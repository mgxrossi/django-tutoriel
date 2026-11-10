Question 4 : personnalisation de l'interface d'administration

Par défaut, Django affiche une liste minimale (question 3). Pour l'améliorer, on crée dans `polls/admin.py` une classe d'administration par modèle, qui hérite de `admin.ModelAdmin` : elle reprend les réglages par défaut et ne modifie que ceux qu'on précise.

Les 4 options utilisées :

| Option | Rôle |

| `list_display` | Colonnes affichées dans la liste (cliquables pour trier) |
| `list_filter` | Panneau de filtres à droite de la liste |
| `ordering` | Ordre de tri par défaut (`-` = ordre décroissant) |
| `search_fields` | Barre de recherche sur les champs indiqués |


from django.contrib import admin

from .models import Choice, Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "question_text", "pub_date"]
    list_filter = ["question_text", "pub_date"]
    ordering = ["-pub_date"]
    search_fields = ["question_text"]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["id", "choice_text", "votes", "question"]
    list_filter = ["question", "choice_text", "votes"]
    ordering = ["question", "-votes"]
    search_fields = ["choice_text", "question__question_text"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
```

`admin.site.register(Question, QuestionAdmin)` indique à Django d'afficher le modèle `Question` avec ces réglages personnalisés.

Résultat : on peut désormais répondre oui aux quatre points de la question 3 :

- tous les attributs sont visibles en colonnes ;
- les données peuvent être filtrées ;
- les colonnes peuvent être triées ;
- une recherche est possible.

Remarques :

- `question__question_text` permet de chercher un choix à partir du texte de sa question (notation double-underscore).
- Le nombre de votes n'est pas inclus dans la recherche, car `search_fields` ne fonctionne qu'avec des champs texte.