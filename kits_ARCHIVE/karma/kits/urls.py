from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views
from .views import WarningListView, UpdateWarningTicketView, PlayerDetailListView, UpdateReviveTicketView, ReviveListView, DeleteReviveTicketView, DeleteWarningTicketView, RulesView, PasswordsChangeView, ServerConfig, GameConfig  # courtesy 

app_name = 'kits'

urlpatterns = [
    path('', views.index, name='index'),
    path('ticket_call/', views.ticket_call, name='ticket_call'),
     path('rules_edit/', views.rules_edit, name='rules_edit'),
    path('getPunishedInfo/', views.getPunishedInfo, name='getPunishedInfo'),
    path('login/', views.login, name='login'),
    path('courtesy/<str:ids>/<str:extra>', views.courtesy, name='courtesy'),
    path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html'), name='change_password'),
    path('warning_list', views.WarningListView.as_view(), name='warning_list'),
    path('revive_list', ReviveListView.as_view(), name='revive_list'),
    path('rules', RulesView.as_view(), name='rules'),
    path('server_config', views.ServerConfig, name='server_config'),
    path('game_config', views.GameConfig, name='game_config'),
    path('player_detail/<int:pk>', PlayerDetailListView.as_view(), name='player_detail'),
    path('kits/tickets_update/<int:pk>', UpdateWarningTicketView.as_view(), name='editticket'),
    path('kits/rtickets_update/<int:pk>', UpdateReviveTicketView.as_view(), name='deleteticket'),
    path('kits/tickets_delete/<int:pk>', DeleteWarningTicketView.as_view(), name='editrticket'),
    path('kits/rtickets_delete/<int:pk>', DeleteReviveTicketView.as_view(), name='deleterticket'),
]
