#! -*- coding: utf-8 -*-
import json

from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from django.utils import timezone

from omnibus.api import publish

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
    # We need to send ping message because of omnibus always lost first message
    publish(
        'mychannel',
        'message',
        {'ping_message': 'ping'},
        sender='server'
    )

    template_name = 'bot.html'

    def process_command(self, cmd, human):
        command = [c for c in Command.objects.all() if c.command in cmd]
        if command:
            method = command[0].method
            user_param = cmd.replace(command[0].command, '').strip()
            message = Executor(method, user_param, human).execute()
            return Bot.objects.create(message=message, date=timezone.now(),
                                      nickname='Бот')

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
            context['history'] = [i.__str__() for i in reversed(history)]
        context['username'] = request.session['human']
        return self.render_to_response(context)

    def post(self, request):
        form = BotForm(data=request.POST)
        if form.is_valid():
            human = request.session['human']
            message = form.data['message']
            date = timezone.now()
            human_message = Bot.objects.create(message=message, date=date,
                                               nickname=human)
            bot_message = self.process_command(message, human)
            data = {'human_message': human_message.__str__()}
            if bot_message:
                data['bot_message'] = bot_message.__str__()
            data = json.dumps(data)

            return HttpResponse(data, content_type='application/json')
        return HttpResponseRedirect('/bot/')
