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