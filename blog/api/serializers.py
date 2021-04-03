from rest_framework import serializers
from blog.models import Post
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_author')
    # date_time_posted = serializers.SerializerMethodField('get_date_posted')

    class Meta:
        model = Post
        fields = ['id','title', 'content', 'username', 'date_posted']
    
    def get_author(self, blog_post):
        username = blog_post.author.username
        return username
    
    # def get_date_posted(self, blog_post):
    #     date_posted = blog_post.date_posted
    #     return date_posted