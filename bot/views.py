#! -*- coding: utf-8 -*-
import json

from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from django.utils import timezone

from .models import Bot, Command
from .forms import HumanForm, BotForm
from .executor import Executor


class HomeView(TemplateView):

    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['form'] = HumanForm()
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        if not request.session.get('human'):
            return self.render_to_response(context)
        return HttpResponseRedirect('/bot')

    def post(self, request):
        form = HumanForm(data=request.POST)
        if form.is_valid():
            human = form.save()
            request.session['human'] = human.username
            return HttpResponseRedirect('/bot/')
        else:
            return HttpResponseRedirect('/')


class BotView(TemplateView):

    template_name = 'bot.html'

    def format_save_message(self, message, name):
        date = timezone.now()
        message = Bot.objects.create(message=message, date=date, nickname=name)
        return message

    def process_comand(self, cmd):
        command = [c for c in Command.objects.all() if c.command in cmd]
        if command:
            method = command[0].method
            user_param = cmd.replace(command[0].command, '').strip()
            message = Executor(method, user_param).execute()
            return self.format_save_message(message, 'Бот')

    def get(self, request, **kwargs):
        human = request.session.get('human')
        context = self.get_context_data()
        last_command = Bot.objects.filter(
            nickname__iexact=human).order_by('-date')
        last_command = last_command[0].message if last_command else None

        context['form'] = BotForm(initial={'message': last_command})
        if not request.session.get('human'):
            return HttpResponseRedirect('/')

        history = Bot.objects.all().order_by('-date')[:5]
        if history:
            context['history'] = [i.__str__() for i in history]
        context['username'] = request.session['human']
        return self.render_to_response(context)

    def post(self, request):
        form = BotForm(data=request.POST)
        if form.is_valid():
            human = request.session['human']
            message = form.data['message']
            human_message = self.format_save_message(message, human).__str__()
            bot_message = self.process_comand(message)
            data = {'human_message': human_message}
            if bot_message:
                data['bot_message'] = bot_message.__str__()
            data = json.dumps(data)

            return HttpResponse(data, content_type='application/json')
        return HttpResponseRedirect('/bot/')
