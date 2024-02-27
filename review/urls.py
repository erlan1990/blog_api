from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentView, RatingView

router = DefaultRouter()
router.register('comments', CommentView)
router.register('ratings', RatingView)

urlpatterns = [
    path('', include(router.urls))
]