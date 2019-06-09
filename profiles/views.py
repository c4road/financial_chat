from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import RegisterForm


class RegisterView(CreateView):

    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('profiles:login')

    def dispatch(self, *args, **kwargs):

        return super(RegisterView, self).dispatch(*args, **kwargs)
