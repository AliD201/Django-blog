from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Deal
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


from django.core.cache import cache
from django_blog.extraContext import getCachedDeals
from django.contrib import messages
import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import permission_required


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
        'deals': deals.objects.all()
    }
    return render(request, 'deal/home.html', context)

# class home view
class DealListView(ListView):
    # required
    model = Deal
    # class views look form app/model_viewtype
    template_name = 'deal/home.html'
    # setting varibles 
    context_object_name = 'deals'
    # change order
    ordering = ['-date_created']
    # this will make it possible to have multiple pages 
    paginate_by = 4
    def dispatch(self, *args, **kwargs):
        # ! here we should fetch the data from the API
        print("dispatching")
        return super().dispatch(*args, **kwargs)
    def get_queryset(self):
        mydata = cache.get('dealsRequest')
        if not mydata:
            mydata = getCachedDeals()[1]
        print(mydata)
        return mydata


def DealDetailView(request, pk):
    if (request.method ==  'GET'):
        mydata = cache.get('dealsRequest')
        if not mydata:
            mydata = getCachedDeals()[1]
        context = {}
        context['canEdit'] = can_edit( request.user)
        context['canDelete'] = canDelete( request.user)
        context['object'] =  list(filter(lambda record: record['id'] == pk, mydata)).pop()
        print(context['object'])
        print('-------------------------------------------------')
        return render(request, 'deal/deal_detail.html', context )
    else:
        if request.user.is_authenticated:
            return redirect('/')
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form} )


# class DealDetailView(DetailView):
#     # required
#     model = Deal

#     def get_queryset(self):
#         mydata = cache.get('dealsRequest')
#         if not mydata:
#             mydata = getCachedDeals()[1]
#         print(mydata)
#         return list(mydata)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['canEdit'] = can_edit( self.request.user)
#         context['canDelete'] = canDelete( self.request.user)
#         return context

    
    # department = get_department(Post.author)
    # def dispatch(self, *args, **kwargs):
    #     print("dispatching")
    #     return super().dispatch(*args, **kwargs)


from .forms import DealCreationForm, DealUpdateForm
class DealCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # class views look form app/model_form
    form_class = DealCreationForm
    model = Deal
    # fields = ['title','price', 'description', 'status', 'date_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'Create'
        return context


    def form_valid(self,form):
        form.instance.handler = self.request.user
        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        if canCreate(user):
            return True
        else:
            return False
    
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            # ! here we should send the data from the API
            print("dispatching - creation")
            form = DealCreationForm(request.POST)
            context = {}
            context['form'] = form
            if form.is_valid():
                newdata = form.cleaned_data
                newdata['value'] = str( form.cleaned_data.get('price'))
                del newdata['handler']
                del newdata['price']
                # ! here we should send the data toward the API
                response = requests.post(f'https://{settings.PIPEDRIVE_DOMAIN}.pipedrive.com/api/v1/deals?api_token={settings.PIPEDRIVE_TOKEN}', newdata) 
                try:
                    response = response.json()
                    print('|||||||||||||||||||||||||||||||||||||||||')
                    print(response)
                    if response['success'] != True:
                        raise Exception()
                except:
                    messages.warning(self.request,f'  Deal Creation failed unexpectedly')
                    return render(request, 'deal/deal_form.html', context )
                messages.success(self.request,f'  Deal Created succefully, may show in around 1 minutes')
            return render(request, 'deal/deal_form.html', context )
        return super().dispatch(request, *args, **kwargs)

@login_required
def DealUpdateView(request, pk):
    if not can_edit(request.user):
        return redirect('deal-detail' , pk=pk)    
    context = {}
    if (request.method ==  'POST'):
        form = DealUpdateForm(request.POST)
        context['form'] = form
        print("before validation")
        if form.is_valid():
            print(form.cleaned_data)
            newdata = form.cleaned_data
            newdata['value'] = str( form.cleaned_data.get('price'))
            newdata['status'] = newdata['status'].lower()
            del newdata['price']
            print(newdata)
            try:
                response = requests.put(f'https://{settings.PIPEDRIVE_DOMAIN}.pipedrive.com/api/v1/deals/{pk}?api_token={settings.PIPEDRIVE_TOKEN}', newdata) 
                response = response.json()
                print(response)
                if response['success'] != True:
                    raise Exception()
            except:
                messages.warning(request,f' Deal updation failed unexpectedly')
                return redirect('deal-detail' , pk=pk)

            messages.success(request,f'  Deal updated succefully, changes may show in around 1 minutes')
            return redirect('deal-detail' , pk=pk)
    else:
        mydata = cache.get('dealsRequest')
        if not mydata:
            mydata = getCachedDeals()[1]
        mydata = list(filter(lambda record: record['id'] == pk, mydata)).pop()
        mydata['status'] = mydata['status'].capitalize()
        form = DealUpdateForm(initial=mydata)
        
        context['form'] = form
        context['form_type'] = 'Update'
    return render(request, 'deal/deal_form.html', context )

#login required and check if the updater is the same user
# class DealUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     # class views look form app/model_form
#     model = Deal
#     form_class = DealUpdateForm
#     # fields = ['title', 'status', 'description']

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form_type'] = 'Update'
#         return context

#     def form_valid(self,form):
#         # form.instance.author = self.request.user
#         form.instance.handler = self.get_object().handler
#         return super().form_valid(form)
    

#     def test_func(self):
#         # post = self.get_object()
#         user = self.request.user
#         return can_edit( user)
#     def dispatch(self, *args, **kwargs):
#         # ! here we should send the data from the API
#         print("dispatching - editing")
#         return super().dispatch(*args, **kwargs)

@login_required
def DealDeleteView(request, pk):
    if not canDelete(request.user):
        return redirect('deal-detail' , pk=pk)   
    context = {}
    if (request.method ==  'POST'):
        try:
            print("in")
            response = requests.delete(f'https://{settings.PIPEDRIVE_DOMAIN}.pipedrive.com/api/v1/deals/{pk}?api_token={settings.PIPEDRIVE_TOKEN}') 
            print("after")
            response = response.json()
            print(response)
            if response['success'] != True:
                raise Exception()
        except:
            messages.warning(request,f' Deal deletion failed unexpectedly')
            return redirect('deal-detail' , pk=pk)
        messages.success(request,f'  Deal deleted succefully, changes may show in around 1 minutes')
        return redirect('deals-home')
    else:
        mydata = cache.get('dealsRequest')
        if not mydata:
            mydata = getCachedDeals()[1]
        mydata = list(filter(lambda record: record['id'] == pk, mydata)).pop()
        
        context['object'] = mydata
        context['form_type'] = 'Delete'
    return render(request, 'deal/deal_confirm_delete.html', context )
    

    
# class DealDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#      # class views look form app/model_form
#     model = Deal

#     success_url = '/deals'
#     def test_func(self):
#         # deal = self.get_object()
#         return canDelete( self.request.user)

#     def dispatch(self, *args, **kwargs):
#         request = kwargs.get("request",self.request)
#         if request.method == "POST":
#             # ! here we should send the data from the API
#             print("Deleting")
#         else:
#             print(request)
#             print("dispatching - deleting")
#         return super().dispatch(*args, **kwargs)





# class home view
class UserDealPostListView(ListView):
    # required
    model = Deal
    # class views look form app/model_viewtype
    template_name = 'deal/user_deals.html'
    # setting varibles 
    context_object_name = 'deals'
    # change order
    ordering = ['-date_created']
    # this will make it possible to have multiple pages 
    paginate_by = 4

    def get_queryset(self):
        mydata = cache.get('dealsRequest')
        if not mydata:
            mydata = getCachedDeals()[1]
        print(mydata)
        return list(filter(lambda record: record['handler'] == self.kwargs.get('username'), mydata))


# def user_is_not_logged_in(user):
#     return not user.is_authenticated()

# @user_passes_test(user_is_not_logged_in)
# def my_view(request):