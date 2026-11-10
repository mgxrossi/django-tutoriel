### Question 3 : observation des interfaces par défaut

Après la saisie des données, les listes *Questions* et *Choices* de l'administration ont été observées.

| Voit-on tous les attributs ? | Non | Une seule colonne est affichée : le texte de l'objet (valeur renvoyée par `__str__`). La date de publication, les votes et la question associée ne sont pas visibles. |
| Peut-on filtrer selon tous les attributs ? | Non | Aucun panneau de filtres n'est proposé. |
| Peut-on trier selon tous les attributs ? | Non | Les en-têtes de colonnes ne sont pas cliquables pour trier. |
| Peut-on chercher un contenu dans tous les champs ? | Non | Aucune barre de recherche n'est disponible. |

Conclusion : l'interface générée par défaut par `admin.site.register()` est minimale. Pour obtenir ces fonctionnalités, il faut la personnaliser avec une classe `ModelAdmin` (question 4).