from rest_framework import serializers

from blog.models import Post, Comment


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'created_date', 'image')


class CommentSerializers(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created_at')
