from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404

from django.views.generic import DetailView, ListView

from .forms import ComposeForm, RoomForm
from .models import Thread, ChatMessage


class InboxView(LoginRequiredMixin, FormMixin, ListView):
    template_name = 'chat/inbox.html'
    form_class = RoomForm
    success_url = '/messages'


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

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        id_  = self.kwargs.get("pk")
        obj = get_object_or_404(Thread, pk=id_)

        return obj


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()

        thread = self.get_object()

        context['chat_messages'] = thread.chatmessage_set.all().order_by('-timestamp')[:50]
        return context

    # def post(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return HttpResponseForbidden()
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    # def form_valid(self, form):
    #     thread = self.get_object()
    #     user = self.request.user
    #     message = form.cleaned_data.get("message")
    #     ChatMessage.objects.create(user=user, thread=thread, message=message)
    #     return super().form_valid(form)


