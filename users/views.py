from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView 
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class SignUpView(CreateView):
    form_class= CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'



class UserDetailView(LoginRequiredMixin,DetailView): 
    model = CustomUser
    template_name = 'user_detail.html'
    context_object_name = 'user'