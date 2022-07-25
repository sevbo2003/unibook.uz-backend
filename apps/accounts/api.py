from rest_framework.viewsets import ModelViewSet
from apps.accounts.serializers import UserSerializer
from apps.accounts.models import User
from apps.accounts.pagination import CustomPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.forum.question.serializers import QuestionSerializer, CommentSerializer
from apps.accounts.permissions import IsUserOrReadOnly
from apps.accounts.filters import UserFilter
from rest_framework import status


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    http_method_names = ['get', 'head', 'patch', 'options']
    permission_classes = [IsUserOrReadOnly]
    pagination_class = CustomPagination
    filterset_class = UserFilter

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request, pk=None):
        if request.user.is_authenticated:
            if request.method == 'GET':
                user = request.user
                serializer = UserSerializer(user)
                return Response(serializer.data)
            elif request.method == 'PATCH':
                user = request.user
                data = request.data
                serializer = UserSerializer(user, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response({"warn": "Please enter valid informations"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
                    
            else:
                return Response({"message": "What do you want to do dude"})
        else:
            return Response({"message": "You should login to see your status"} ,status=status.HTTP_404_NOT_FOUND)
    

    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        user = self.get_object()
        serializer = QuestionSerializer(user.question_set.all(), many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        user = self.get_object()
        serializer = QuestionSerializer(user.likes.all(), many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def answers(self, request, pk=None):
        user = self.get_object()
        serializer = CommentSerializer(user.comment_set.all(), many=True)
        return Response(serializer.data)


# class QuestionViewSet(viewsets.ModelViewSet):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#     permission_classes = [IsAuthorOrReadOnly]
#     filter_backends = [OrderingFilter]

#     def retrieve(self, request, *args, **kwargs):
#         object = self.get_object()
#         path_obj = request.path.replace('/', '')
#         value = request.COOKIES.get(f"{path_obj}_view_count")
#         if value is None:
#             object.view_count += 1
#             object.save()
#             response = super().retrieve(request, *args, **kwargs)
#             response.set_cookie(f"{path_obj}_view_count", path_obj)
#             return response
#         return super().retrieve(request, *args, **kwargs)

