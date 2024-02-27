from rest_framework.serializers import ModelSerializer, ValidationError, Serializer, CharField, ReadOnlyField

from .models import Post, Tag, Category
from review.serializer import CommentSerializer
from review.models import Comment
from django.db.models import Avg

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title',)

class Tags(Serializer):
    title = CharField(required=True)
    test = CharField(required=True)

    def validate(self, attrs):
        ...

    def validate_title(self, title):
        ...

    def create(self, validated_data):
        ...

    def update(self, validated_data):
        ...

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('title',)

class PostSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.name')
    class Meta:
        model = Post
        fields = '__all__'

    def validate_title(self, title):
        if self.Meta.model.objects.filter(title=title).exists():
            raise ValidationError(
                'Заголовок не должен повторяться'
            )
        return title
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation['test'] = 'test'
        # representation['tags'] = instance.tags.all().count()
        # representation['comments'] = CommentSerializer (instance.comments.all(), many=True).data
        representation['comments'] = CommentSerializer (Comment.objects.filter(post=instance.pk), many=True).data
        representation['rating'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        representation['likes'] = instance.likes.count()
        return representation
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['author'] = user
        return super().create(validated_data)
    

        # print('==============')
        # print(user)
        # print('=================')
        # tags = validated_data.pop('tags', [])
        # post = Post.objects.create(author=user, **validated_data)
        # post.tags.add(*tags)
        # return post
    

    # def create(self, validated_data):
    #     tags = validated_data.pop(tags, [])
    #     print(tags)
    #     post = self.Meta.model.objects.create(**validated_data)
    #     post.tags.add(tags)
    #     return post
        


class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'author']

