#! -*- coding: utf-8 -*-
import datetime
import json

from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView

from .models import Bot, Command
from .forms import HumanForm, BotForm
from .executor import Executor


class HomeView(TemplateView):

    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['form'] = HumanForm()
        return context

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

    def format_message(self, message, name):
        date = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        return ' '.join([date, name, '\b:', str(message)])

    def process_comand(self, cmd, username):
        command = [c for c in Command.objects.all() if c.command in cmd]
        if command:
            method = command[0].method
            user_param = cmd.replace(command[0].command, '').strip()
            message = Executor(method, user_param).execute()
            return self.format_message(message, 'Бот')

    def get_context_data(self, **kwargs):
        context = super(BotView, self).get_context_data(**kwargs)
        last_command = Bot.objects.last()
        last_command = last_command.command if last_command else None

        context['form'] = BotForm(initial={'command': last_command})
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data()
        if not request.session.get('human'):
            return HttpResponseRedirect('/')

        context['username'] = request.session['human']
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        form = BotForm(data=request.POST)
        if form.is_valid():
            command = form.save()
            human = request.session['human']

            human_message = self.format_message(command.command, human)
            message = self.process_comand(command.command, human)

            data = json.dumps({'message': message,
                               'command': human_message})

            return HttpResponse(data, content_type='application/json')
        return HttpResponseRedirect('/bot/')
