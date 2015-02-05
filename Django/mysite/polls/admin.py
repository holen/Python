from django.contrib import admin
from polls.models import Question, Choice

#class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3 

class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question_text']
    #fieldsets = [
#	('Question', {'fields':['question_text']}),
#	('Date information', {'fields': ['pub_date'], 'classes':['collapse']}),
#    ]
#    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date')
    list_filter = ['pub_date']
    search_fields = [ 'question_text' ]
    #list_display = ('question_text', 'pub_date', 'was_published_recently')

# Register your models here.
#admin.site.register(Question)
admin.site.register(Question, QuestionAdmin)
#admin.site.register(Choice)
