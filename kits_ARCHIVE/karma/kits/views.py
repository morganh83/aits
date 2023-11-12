from http.client import HTTPResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from . import models
from django.urls import reverse, reverse_lazy
from .forms import TicketsForm, RTicketsForm, ConfigForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from kits.models import Rule, dinoName, banLength, strikeType, revTicket, punishTicket, brokenRules
from django.db.models import Q, CharField
from django.views.decorators.csrf import csrf_exempt
import json, aiohttp, discord, html2text, requests, os, datetime
from discord import SyncWebhook, Embed

def login(request):
    return render(request, 'kits/login.html')

@login_required
def GameConfig(request):
    # Game Config File
    # config_file =  'S:\Servers\BoB\WindowsServer\BeastsOfBermuda\Saved\Config\WindowsServer\Game.ini'
    config_file = '/ticketApp/database/game/game.ini'
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if request.method == 'POST':
        form = ConfigForm(request.POST)
        if form.is_valid():
            os.rename(config_file, config_file + "_" + dt + ".ini")
            with open(config_file, 'w') as f:
                f.write(form.cleaned_data.get('config'))
                f.close()
            return redirect('kits:game_config')
    else:
        form = ConfigForm()
        f = open(config_file, 'r+')
        file_content = f.read()
        f.close()
        form.fields['config'].initial = file_content
        return render(request, 'kits/server_config.html', {'form': form})

@login_required
def ServerConfig(request):
    # Server Config File
    # config_file = 'S:\Utils\Server Watchdog\server.settings'
    config_file = '/ticketApp/database/server/server.settings'
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if request.method == 'POST':
        form = ConfigForm(request.POST)
        if form.is_valid():
            os.rename(config_file, config_file + "_" + dt + ".settings")
            with open(config_file, 'w') as f:
                f.write(form.cleaned_data.get('config'))
                f.close()
            return redirect('kits:server_config')
    else:
        form = ConfigForm()
        f = open(config_file, 'r+')
        file_content = f.read()
        f.close()
        form.fields['config'].initial = file_content
        return render(request, 'kits/server_config.html', {'form': form})

class ReviveListView(LoginRequiredMixin, ListView):
    model = revTicket
    template_name = 'kits/revive_list.html'
    paginate_by = 50
    def get_queryset(self):
        searched = self.request.GET.get('revsearched')
        object_list = revTicket.objects.order_by('-createdAt')
        if searched:
            object_list = revTicket.objects.filter(
                Q(modName__icontains=searched) | 
                Q(steamId__icontains=searched) | 
                Q(userName__icontains=searched) | 
                Q(discName__icontains=searched) | 
                Q(dinoName__icontains=searched)
            ).order_by('-createdAt')
        return object_list
    def get_context_data(self, **kwargs):
        context = super(ReviveListView, self).get_context_data(**kwargs)
        return context

class WarningListView(LoginRequiredMixin, ListView):
    model = punishTicket
    context_object_name = 'all_warnings'
    template_name = 'kits/warning_list.html'
    paginate_by = 50
    def get_queryset(self):
        searched = self.request.GET.get('searched')
        object_list = punishTicket.objects.order_by('-createdAt')
        if searched:
            object_list = punishTicket.objects.filter(
                Q(modName__icontains=searched) |
                Q(punishment__icontains=searched) |
                Q(steamId__icontains=searched) |
                Q(discName__icontains=searched) |
                Q(banTime__icontains=searched) |
                Q(userName__icontains=searched)
            ).order_by('-createdAt')
        return object_list
    
    def get_context_data(self, **kwargs):
        context = super(WarningListView, self).get_context_data(**kwargs)
        return context

class PlayerDetailListView(LoginRequiredMixin, DetailView):
    model = punishTicket
    context_object_name = 'all_PlayerTickets'
    queryset = punishTicket.objects.order_by('-createdAt')
    template_name = 'kits/player_detail.html'

def rules_edit(request):
    if request.method == "POST":
        all_rules = json.loads(request.body)
        current_ticket = punishTicket.objects.get(pk=all_rules['id'])
        current_ticket.brokenRules.all().delete()
        for rule in all_rules['rules'][1:]:
            current_rule = Rule.objects.get(rules=rule)
            current_ticket.brokenRules.create(rules=rule, description=current_rule.description, clarity=current_rule.clarity)
        return JsonResponse({"response": 200})
    return JsonResponse({"response": 500})    

class UpdateWarningTicketView(LoginRequiredMixin, UpdateView):
    model = punishTicket
    template_name = 'kits/warning_edit.html'
    form_class = TicketsForm
    success_url = reverse_lazy('kits:warning_list')
    ban_list = banLength.objects.all()
    strike_list = strikeType.objects.all()
    def get_context_data(self, **kwargs):
        context = super(UpdateWarningTicketView, self).get_context_data(**kwargs)
        saving_ticket = punishTicket.objects.get(pk=self.kwargs['pk'])
        excluded_rules = ['None']
        for rule in saving_ticket.brokenRules.all():
            excluded_rules.append(rule.rules)
        rule_list = Rule.objects.exclude(rules__in=excluded_rules)
        excluded_rule_list = Rule.objects.filter(rules__in=excluded_rules)
        if self.request.POST:
            data = self.request.POST
            saving_ticket.userName = data.get('userName') if data.get('userName') else saving_ticket.userName
            saving_ticket.steamId = data.get('steamId') if data.get('steamId') else saving_ticket.steamId
            saving_ticket.discName = data.get('discName') if data.get('discName') else saving_ticket.discName
            saving_ticket.punishment = data.get('punishment') if data.get('punishment') else saving_ticket.punishment
            saving_ticket.banTime = data.get('banTime') if data.get('banTime') else saving_ticket.banTime
            saving_ticket.banTime = data.get('banTimeOther') if data.get('banTimeOther') else saving_ticket.banTimeOther
            saving_ticket.reason = data.get('reason') if data.get('reason') else saving_ticket.reason
            saving_ticket.ticketLink = data.get('ticketLink') if data.get('ticketLink') else saving_ticket.ticketLink
            saving_ticket.counterLink = data.get('counterLink') if data.get('counterLink') else saving_ticket.counterLink
            saving_ticket.addtlMods = data.get('addtlMods') if data.get('addtlMods') else saving_ticket.addtlMods
            saving_ticket.save()

        context['ban_list'] = self.ban_list
        context['strike_list'] = self.strike_list
        context['rule_list'] = rule_list
        context['excluded_rule_list'] = excluded_rule_list
        context['broken_list'] = saving_ticket.brokenRules.all()
        return context

class DeleteWarningTicketView(LoginRequiredMixin, DeleteView):
    model = punishTicket
    fields = "__all__"
    template_name = 'kits/warning_edit.html'
    form_class = TicketsForm
    success_url = reverse_lazy('kits:warning_list')

class UpdateReviveTicketView(LoginRequiredMixin, UpdateView):
    model = revTicket
    template_name = 'kits/revive_edit.html'
    form_class = RTicketsForm
    success_url = reverse_lazy('kits:revive_list')
    dino_list = dinoName.objects.all()
    def get_context_data(self, **kwargs):
        context = super(UpdateReviveTicketView, self).get_context_data(**kwargs)
        if self.request.POST:
            data = self.request.POST
            saving_ticket = revTicket.objects.get(pk=self.kwargs['pk'])
            saving_ticket.userName = data.get('userName') if data.get('userName') else saving_ticket.userName
            saving_ticket.steamId = data.get('steamId') if data.get('steamId') else saving_ticket.steamId
            saving_ticket.discName = data.get('discName') if data.get('discName') else saving_ticket.discName
            saving_ticket.growth = data.get('growth') if data.get('growth') else saving_ticket.growth
            saving_ticket.dinoName = data.get('dinoName') if data.get('dinoName') else saving_ticket.dinoName
            saving_ticket.revd = True if data.get('revd') else False
            saving_ticket.ticketLink = data.get('ticketLink') if data.get('ticketLink') else saving_ticket.ticketLink
            saving_ticket.counterLink = data.get('counterLink') if data.get('counterLink') else saving_ticket.counterLink
            saving_ticket.addtlMods = data.get('addtlMods') if data.get('addtlMods') else saving_ticket.addtlMods
            saving_ticket.save()
        context['dino_list'] = self.dino_list
        return context

class DeleteReviveTicketView(LoginRequiredMixin, DeleteView):
    model = revTicket
    fields = "__all__"
    template_name = 'kits/revive_edit.html'
    form_class = RTicketsForm
    success_url = reverse_lazy('kits:revive_list')

class RulesView(ListView):
    model = Rule
    context_object_name = 'all_rules'
    queryset = Rule.objects.order_by('rules')
    template_name = 'kits/pub/rules.html'

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('kits:index')


def ticket_call(request):
    courtesies = []
    if request.method == 'POST':
        ticket_data = json.loads(request.body)
        modInput = request.user
        if ticket_data['revive']:
            for rev in ticket_data['revive'].values():
                new_rev = revTicket(
                    userName=rev['username'], 
                    discName=rev['discordID'],
                    steamId=rev['steamID'],
                    growth=rev['growth'], 
                    dinoName=rev['dino'],
                    revd=rev['revive'], 
                    modName=modInput, 
                    ticketLink=ticket_data['ticketLink'],
                    counterLink=ticket_data['counterLink'], 
                    addtlMods=ticket_data['additionalMods'])

                new_rev.save()
        if ticket_data['punish']:
            for pun in ticket_data['punish'].values():

                new_pun = punishTicket(
                    userName=pun['username'], 
                    discName=pun['discordID'],
                    steamId=pun['steamID'], 
                    punishment=pun['punishment'], 
                    banTime=pun['banLength'], 
                    banTimeOther=pun['otherBanLength'], 
                    reason=pun['reason'],
                    modName=modInput, 
                    ticketLink=ticket_data['ticketLink'],
                    counterLink=ticket_data['counterLink'], 
                    addtlMods=ticket_data['additionalMods'])

                new_pun.save()
                if pun['discordID']:
                    courtesies.append(str(new_pun.id))

                if pun['brokenRules']:
                    for rule in pun['brokenRules']:
                        rule_id = Rule.objects.get(rules=rule)
                        new_pun.brokenRules.create(
                            rules=rule_id.rules, 
                            description=rule_id.description, 
                            clarity=rule_id.clarity)
    if courtesies:
        sent_data = "|".join(courtesies)
    else:
        sent_data = None
    return JsonResponse({'courtesies': sent_data})


def getPunishedInfo(request):

    if request.method == 'GET':
        id_get = request.GET['id']
        response = {}

        users = punishTicket.objects.filter(steamId=id_get).order_by('-id')
        count = users.count()
        if count == 0:
            response = {
                'error': 'ID does not exist'
            }
        else:
            response['punishCount'] = count
            users_arr = []
            for user in users:
                link = ''
                link_test = False
                if user.counterLink:
                    if not user.counterLink == "":
                        link = 'countered'
                users_arr.append(
                    [user.createdAt, [link, link_test], user.punishment, user.discName])
            response['users'] = users_arr

    return JsonResponse(response)

def send_message(message):
    webhook = SyncWebhook.from_url('https://discord.com/api/webhooks/1023694324170489857/sKiYlH6tsGRCjixoliQrD7iQ-2A3Lzf_h7c4RG2Uzt_6xdoXuttReJdxLUebupqZA34w')
    webhook.send(content=html2text.html2text(message))

@login_required
def courtesy(request, ids, extra):

    objects = []
    thanks_obj = []
    thanks = False
    if ids == "none":
        thanks = True
        if not extra == '0':
            thanks_arr = extra.split('|') 
            for pun_id in thanks_arr:
                current_courtesy = punishTicket.objects.filter(id=int(pun_id)).first()
                thanks_obj.append([current_courtesy.userName ,current_courtesy.discName])
    else:
        id_arr = ids.split('|')
        for pun_id in id_arr:
            current_courtesy = punishTicket.objects.filter(id=int(pun_id)).first()
            broken_rules = brokenRules.objects.filter(user=int(pun_id))
            all_rules = []
            for rule in broken_rules:
                rule_ = rule.rules
                description = rule.description
                all_clarities = rule.clarity.split('•') 
                for clarity in all_clarities:
                    all_clarities[all_clarities.index(clarity)] = ' • ' + clarity
                del all_clarities[0]
                all_rules.append([rule_, description, all_clarities])
            objects.append([current_courtesy, all_rules])

    if request.method == "POST":
        for i in range (1, len(id_arr) + 1):
            punished_user = punishTicket.objects.filter(id=id_arr[i-1]).first()
            new_message = f'<p>!courtesymessage <@{punished_user.discName}></p>' + request.POST.get('form' + str(i))
            send_message(new_message)
            punished_user.courtesy = True
            punished_user.save()

        return redirect('/courtesy/none/' + ids)

    return render(request, 'kits/courtesy.html', context={'courtesies': objects, 'thanks': thanks, 'thanks_obj': thanks_obj})

@login_required
def index(request):

    rules_list = Rule.objects.all()
    dino_list = dinoName.objects.all()
    ban_list = banLength.objects.all()
    strike_list = strikeType.objects.all()
    return render(request, 'kits/newticket.html', context={'rule_list': rules_list, 'dino_list': dino_list, 'ban_list': ban_list, 'strike_list': strike_list})
