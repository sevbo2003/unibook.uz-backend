from rest_framework import viewsets
from apps.forum.question.serializers import MainCategorySerializer, SubCategorySerializer, QuestionSerializer, CommentSerializer
from apps.accounts.serializers import UserSerializer
from apps.forum.question.models import MainCategory, SubCategory, Question, Comment
from apps.forum.question.permissions import IsAuthorOrReadOnly, is_question_owner
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


class MainCategoryViewSet(viewsets.ModelViewSet):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return [IsAdminUser()]
        return [permission() for permission in self.permission_classes]


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return [IsAdminUser()]
        return [permission() for permission in self.permission_classes]
        

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        if self.request.GET.get('sort'):
            x = self.request.GET.get('sort')
            if x == 'top':
                return Question.objects.order_by('-answers_count')
            elif x == 'newest':
                return Question.objects.order_by('-creation_date')
            elif x == 'oldest':
                return Question.objects.order_by('creation_date')
            print("Worked")
            return Question.objects.order_by('-creation_date')
        if self.request.GET.get('category'):
            x = self.request.GET.get('category')
            return Question.objects.filter(main_category__slug=x)
        return Question.objects.order_by('-creation_date')

    def retrieve(self, request, *args, **kwargs):
        object = self.get_object()
        path_obj = request.path
        value = request.COOKIES.get('link_url')
        if value is None:
            object.view_count += 1
            object.save()
            response = super().retrieve(request, *args, **kwargs)
            response.set_cookie('link_url', path_obj)
            return response
        return super().retrieve(request, *args, **kwargs)
            

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
    
    @action(detail=True)
    def answers(self, request, pk=None):
        if request.GET.get('id'):
            answer = Comment.objects.get(id=request.GET.get('id'))
            serializer = CommentSerializer(answer)
            return Response(serializer.data)
        question = self.get_object()
        serializer = CommentSerializer(question.comment_set.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET', 'POST'])
    def likes(self, request, pk=None):
        question = self.get_object()
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(question.likes.all(), many=True)
            return Response(serializer.data)
        else:
            if user in question.likes.all():
                return Response({"message": "Already liked"})
            else:
                question.likes.add(user)
                question.user.reputation += 1
                question.user.save()
                question.save()
                return Response({"message": "liked"})
    
    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        question = self.get_object()
        user = request.user
        if user in question.likes.all():
            question.likes.remove(user)
            question.user.reputation -= 1
            question.user.save()
            question.save()
            return Response({"message": "unliked"})
        return Response({"message": "Not liked"})

    def get_permissions(self):
        if self.action == 'likes' or self.action == 'unlike':
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(is_active=True)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        data = self.request.data
        ques = Question.objects.get(id=data['question'])
        ques.answers_count += 1
        ques.save()
        return super().perform_create(serializer)

    @action(detail=True)
    def replies(self, request, pk=None):
        comment = self.get_object()
        serializer = CommentSerializer(comment.replies.all(), many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET', 'POST'])
    def likes(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(comment.likes.all(), many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            if user not in comment.likes.all():
                comment.likes.add(user)
                comment.user.reputation += 1
                comment.user.save()
                comment.save()
                return Response({"message": 'Liked'})
            return Response({"message": 'Already Liked'})
        return Response(status=201)
     
    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        if user in comment.likes.all():
            comment.likes.remove(user)
            comment.user.reputation -= 1
            comment.user.save()
            comment.save()
            return Response({"message": "unliked"})
        return Response({"message": "Not liked"})

    @action(detail=True, methods=['POST'])
    def true(self, request, pk=None):
        comment = self.get_object()
        x = is_question_owner(request.user, comment)
        if x:
            if comment.question.has_true_answer == False:
                comment.is_true_answer = True
                comment.question.has_true_answer = True
                comment.user.reputation += 3
                comment.save()
                comment.question.save()
                comment.user.save()
                return Response({"message": "This answer marked as a true answer"})
            return Response({"message": "This question already has true answer"})
        return Response({"message": "You are not the owner of this question"})

    def get_permissions(self):
        if self.action == 'likes' or self.action == 'unlike' or self.action == 'true':
            if self.request.method == 'POST':
                return [IsAuthenticated()]
            return []
        elif self.action == 'replies':
            return [IsAuthorOrReadOnly()]
        return [permission() for permission in self.permission_classes]
