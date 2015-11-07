#! -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect
from django.views.generic import TemplateView

from .forms import HumanForm, BotForm


class HomeView(TemplateView):

    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['form'] = HumanForm()
        return context

    def post(self, request):
        form = HumanForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bot/')
        else:
            return HttpResponseRedirect('/')


class BotView(TemplateView):

    template_name = 'bot.html'

    def get_context_data(self, **kwargs):
        context = super(BotView, self).get_context_data(**kwargs)
        context['form'] = BotForm()
        return context

