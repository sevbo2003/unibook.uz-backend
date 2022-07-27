from apps.forum.question.models import MainCategory, SubCategory, Question, Comment
from rest_framework import serializers
from apps.accounts.serializers import UserSerializer


class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name", 'slug', "main_category"]
        read_only_fields = ['slug']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "title", "body", "user", "main_category", "sub_category", "creation_date", "has_true_answer","view_count", "answers_count", "likes_count"]
        read_only_fields = ["creation_date", "view_count", "answers_count", "likes_count", "has_true_answer", "user"]

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'question', 'user', 'likes_count', 'body', 'creation_date', 'is_true_answer', 'is_active', 'parent', 'score']
        read_only_fields = ['score', 'is_true_answer', 'creation_date', 'likes_count', 'is_active', "user"]
    
    def create(self, validated_data):
        question = validated_data['question']
        item = Question.objects.get(id = question.id)
        item.answers_count += 1
        item.save()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance