from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

# from rest_framework.authentication import TokenAuthentication

from rest_framework_simplejwt.authentication import JWTAuthentication 

from django_blog.roles import CanEdit as can_edit
from django_blog.roles import canCreate


from django.contrib.auth.models import User
from blog.models import Post 
from .serializers import PostSerializer

from django.utils import timezone
import datetime




# class PostDetailView(DetailView, APIView):
#     # required
#     model = Post



@api_view(['GET',])
@permission_classes([IsAuthenticated])
def post_detail(request, id):
    try:
        blog_post = Post.objects.get(id = id)
        print( blog_post)
    except :
        return Response(status= status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PostSerializer(blog_post)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes([IsAuthenticated])
def post_update(request, id):
    try:
        blog_post = Post.objects.get(id = id)
        print( blog_post.__dict__)
    except :
        return Response(status= status.HTTP_404_NOT_FOUND)

    user = request.user
    if not can_edit( user):
            return Response( {'response': "You don't have permission to edit this post "})

    if request.method == 'PUT':
        serializer = PostSerializer(blog_post, data= request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "updated succefully"
            return Response(data = data)
        return Response(serializer.errors, status =status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes([IsAuthenticated])
def post_delete(request, id):
    try:
        blog_post = Post.objects.get(id = id)
        print( blog_post)
    except :
        return Response(status= status.HTTP_404_NOT_FOUND)
    
    user = request.user
    if not can_edit( user):
            return Response( {'response': "You don't have permission to edit this post "})

    if request.method == 'DELETE':
        operation = blog_post.delete()
        data = {}
        if operation:
            data['success'] = "deleted succefully"
        else:
            data ['failure'] = 'delete failed'
        return Response(data = data)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def post_create(request):
    user = request.user
    blog_post = Post(author=user)
    blog_post.date_posted = now = datetime.datetime.now().isoformat(sep='T') + 'Z'

    if not canCreate(user):
        return Response( {'response': "You don't have permission to create a new post "})

    if request.method == 'POST' :
        serializer = PostSerializer(blog_post, data= request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# we will change the base and use now a class based views 
class post_list_view(ListAPIView):
    queryset = Post.objects.all()
    
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = ( SearchFilter, OrderingFilter)
    search_fields = ('title', 'content', 'author__username', 'date_posted')
 

    # ordering_fields = ['title', 'author','date_posted']
    # ordering = ['-date_posted']

# @api_view(['GET', 'POST'])
# def posts_list(request, id):
#     try:
#         blog_post = Post.objects.all()
#         print(blog_post)
#     except Post.DoesNotExist:
#         return Response(status= status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = PostSerializer(blog_post)
#         return Response(serializer.data)

# @api_view(['GET', 'POST'])
# def api_posts_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)