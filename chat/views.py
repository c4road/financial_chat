from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .forms import ComposeForm, RoomForm
from .models import Thread


class InboxView(LoginRequiredMixin, FormMixin, ListView):
    template_name = 'chat/inbox.html'
    form_class = RoomForm
    success_url = '/rooms'

    def get_queryset(self):
        return Thread.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        name = form.cleaned_data.get("name")
        Thread.objects.create(name=name)
        return super().form_valid(form)


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/thread.html'
    form_class = ComposeForm
    success_url = './'

    def get_object(self):
        id_ = self.kwargs.get("pk")
        obj = get_object_or_404(Thread, pk=id_)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()

        thread = self.get_object()

        context['chat_messages'] = thread.chatmessage_set.all().order_by(
            '-timestamp')[:50]
        return context
