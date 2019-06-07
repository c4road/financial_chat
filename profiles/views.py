from django.shortcuts import render
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from .forms import RegisterForm



class RegisterView(CreateView):

	form_class = RegisterForm
	template_name = 'registration/register.html'
	success_url = reverse_lazy('profiles:login')

	def dispatch(self, *args, **kwargs):

		return super(RegisterView, self).dispatch(*args, **kwargs)


# class LoginView(FormView):

# 	form_class = AuthenticationForm
# 	template_name = 'registration/login.html'


