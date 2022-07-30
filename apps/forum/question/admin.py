from django.contrib import admin
from apps.forum.question.models import MainCategory, SubCategory, Question, Comment

admin.site.register(MainCategory)
admin.site.register(SubCategory)
admin.site.register(Question)
admin.site.register(Comment)
