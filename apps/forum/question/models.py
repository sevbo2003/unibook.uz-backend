import imp
from django.db import models
from apps.accounts.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db.models.signals import m2m_changed


class MainCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    # @property
    # def sub_categories(self):
    #     return self.subcategory_set.all()

    class Meta:
        verbose_name = 'Main Category'
        verbose_name_plural = 'Main Categories'


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            super().save(*args, **kwargs)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'


class Question(models.Model):
    title = models.CharField(max_length=500)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    sub_category = models.ManyToManyField(SubCategory)
    creation_date = models.DateTimeField(auto_now_add=True)
    has_true_answer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    answers_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.answers_count = self.comment_set.all().count()
        return super().save(*args, **kwargs)
    
    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def top_score(self):
        return self.answers_count + self.likes_count

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['-creation_date']


def sub_category_changed(sender, **kwargs):
    if kwargs['instance'].sub_category.count() > 3:
        raise ValidationError("You can choose up to 3 sub category")

m2m_changed.connect(sub_category_changed, sender=Question.sub_category.through)


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    body = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    is_true_answer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def score(self):
        return self.likes.count()

    def __str__(self) -> str:
        return str(self.user) + ': ' +str( self.question.title) + ': ' + str(self.score)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-creation_date']