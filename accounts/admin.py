from django.contrib import admin

from .models import *

from . import models
# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(Mentor)
admin.site.register(Mentee)
admin.site.register(Match)
admin.site.register(Goal)
admin.site.register(Session)
admin.site.register(Task)
admin.site.register(Ad)
admin.site.register(Ad2)
admin.site.register(Result)

@admin.register(models.Category)

class QuizAdmin(admin.ModelAdmin):
	list_display = [
        'name',
        ]


@admin.register(models.Quizzes)

class QuizAdmin(admin.ModelAdmin):
	list_display = [
        'id', 
        'title',
        ]


class AnswerInlineModel(admin.TabularInline):
    model = models.Answer
    fields = [
        'answer_text', 
        'is_right'
        ]


@admin.register(models.Question)

class QuestionAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'quiz',
        ]
    list_display = [
        'title', 
        'quiz',
        'date_updated'
        ]
    inlines = [
        AnswerInlineModel, 
        ] 


@admin.register(models.Answer)

class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'answer_text', 
        'is_right', 
        'question'
        ]