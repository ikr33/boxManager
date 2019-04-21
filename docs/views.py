from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,\
    UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)





# Create your views here.

def home(request):
    context = {

    }
    return render(request,'docs/home.html',context)




# this class requires the following template by default,
# but we override  template name with home.html
#<app>/<model>_<viewtype>.html, something like: blog/post_list.html
class DocListView(ListView):
    model = User
    template_name = 'docs/home.html'

class MainListView(ListView):
    model = User
    template_name = 'docs/main.html'




class DocDetailView(DetailView):
    model = User




def about(request):

    return render(request, 'docs/about.html',{'title':"About"})