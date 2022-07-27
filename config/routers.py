from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.accounts.api import UserViewSet
from apps.forum.question.api import MainCategoryViewSet, SubCategoryViewSet, QuestionViewSet, CommentViewSet

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("main-categories", MainCategoryViewSet)
router.register("sub-categories", SubCategoryViewSet)
router.register("questions", QuestionViewSet)
router.register("comments", CommentViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
