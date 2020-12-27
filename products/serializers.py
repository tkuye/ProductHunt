from rest_framework import serializers
from products.models import Comment

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['username', 'comment']

