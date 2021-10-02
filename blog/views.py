from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django_blog.decorators import group_check
# from django_blog.helpers import get_department, can_edit
from django_blog.roles import CanEdit as can_edit
from django_blog.roles import canCreate
from django_blog.roles import canDelete
# class views 
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

# posts = [
#     {
#         'author':'Ali',
#         'title' : 'first blog',
#         'content': 'this is a greate place',
#         'date_posted': 'August 27, 2018'
#     },
#     {
#         'author':'Moh',
#         'title' : 'second blog',
#         'content': ' Sconed, this is a greate place',
#         'date_posted': 'August 27, 2018'
#     },
    
# ]


def home (request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

# class home view
class PostListView(ListView):
    # required
    model = Post
    # class views look form app/model_viewtype
    template_name = 'blog/home.html'
    # setting varibles 
    context_object_name = 'posts'
    # change order
    ordering = ['-date_posted']
    # this will make it possible to have multiple pages 
    paginate_by = 4
  

def about (request):
    return render(request, 'blog/about.html', {'title': 'About'})



class PostDetailView(DetailView):
    # required
    model = Post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['canEdit'] = can_edit( self.request.user)
        context['canDelete'] = canDelete( self.request.user)
        return context

    # department = get_department(Post.author)
    # def dispatch(self, *args, **kwargs):
    #     print("dispatching")
    #     return super().dispatch(*args, **kwargs)



class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # class views look form app/model_form
    model = Post
    fields = ['title', 'content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        if canCreate(user):
            return True
        else:
            return False


    

#login required and check if the updater is the same user
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # class views look form app/model_form
    model = Post
    fields = ['title', 'content']


    def form_valid(self,form):
        # form.instance.author = self.request.user
        form.instance.author = self.get_object().author
        return super().form_valid(form)
    

    def test_func(self):
        # post = self.get_object()
        user = self.request.user
        return can_edit( user)

  
    

    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
     # class views look form app/model_form
    model = Post

    success_url = '/'
    def test_func(self):
        post = self.get_object()
        return canDelete( self.request.user)




# class home view
class UserPostListView(ListView):
    # required
    model = Post
    # class views look form app/model_viewtype
    template_name = 'blog/user_posts.html'
    # setting varibles 
    context_object_name = 'posts'
    # change order
    ordering = ['-date_posted']
    # this will make it possible to have multiple pages 
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# def user_is_not_logged_in(user):
#     return not user.is_authenticated()

# @user_passes_test(user_is_not_logged_in)
# def my_view(request):