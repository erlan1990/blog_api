
from rest_framework.views import APIView
from .models import Category, Tag, Post
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import CursorPagination
from rest_framework.decorators import action
from review.models import Like
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .permissions import IsAuthorPermission



# class PostsView(APIView):

#     def get(self, request):
#         queryset = Post.objects.all()
#         serializer = PostSerializer(queryset, many=True)
#         return Response(serializer.data, status=200)
    
#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=201)

# # python3 manage.py makemigrations
# # python3 manage.py migrate

class TagView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser]

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

# class PostView(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_fields = ['category', 'tags', 'title']
#     search_fields = ['title', 'body']
#     ordering_fields = ['title']
#     # serializer_class = PostSerializer

#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return PostListSerializer
#         return PostSerializer

# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
    
class CustomCursorPagination(CursorPagination):
    page_size = 3
    ordering = '-created_at'


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'tags', 'title']
    search_fields = ['title', 'body']
    # ordering_fields = ['title']
    pagination_class = CustomCursorPagination

    def get_permissions(self):
        if self.action in ['list', 'retrive']:
            permissions = [AllowAny]
        elif self.action == 'create':
            permissions = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission]
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return self.serializer_class
    
    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, author=user)
            like.delete()
            message = 'disliked'
        except Like.DoesNotExist:
            like = Like.objects.create(post=post, author=user)
            message = 'liked'
        
        return Response(message, status=200)
