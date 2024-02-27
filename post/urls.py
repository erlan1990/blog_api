from django.urls import path, include
from .views import TagView, CategoryView, PostViewSet
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('posts', PostViewSet)

print(router.urls)

urlpatterns = [
    # path('posts/', PostView.as_view()),
    # path('posts/<slug:pk>/', PostDetailView.as_view()),
    path('tags/', TagView.as_view()),
    path('categories/', CategoryView.as_view()),
    # path('', include(router.urls))

    path('posts/', PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-list'),
    path('posts/<slug:pk>/', PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),name='post_detail')
]
