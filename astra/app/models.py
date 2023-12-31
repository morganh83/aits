from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    discord_id = models.CharField(max_length=100, blank=True, null=True)
    steam_id = models.CharField(max_length=100, blank=True, null=True)
    admin_group = models.BooleanField(default=False)
    admin_plus_group = models.BooleanField(default=False)
    moderator_group = models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.username

class dinoName(models.Model):
    dino = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.dino


class strikeType(models.Model):
    strike = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.strike


class banLength(models.Model):
    banLen = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.banLen


class Rule(models.Model):
    rules = models.CharField(max_length=6, unique=True)
    description = models.CharField(max_length=400, unique=True)
    clarity = models.TextField(max_length=2000, default="", blank=True)

    def __str__(self):
        return f"{self.rules} - {self.description}"


class revTicket(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    modName = models.CharField(max_length=100, default="", null=True, blank=True)
    addtlMods = models.CharField(max_length=100, default="", null=True, blank=True)
    userName = models.CharField(max_length=200, default="", null=True, blank=True)
    discName = models.CharField(max_length=100, default="", null=True, blank=True)
    steamId = models.IntegerField(default=0, null=True, blank=True)
    growth = models.CharField(max_length=6, default="", null=True, blank=True)
    dinoName = models.CharField(max_length=30, null=True, blank=True, default="")
    revd = models.BooleanField(default=False, blank=True)
    ticketLink = models.CharField(max_length=500, default="", null=True, blank=True)
    counterLink = models.CharField(max_length=500, default="", null=True, blank=True)


class punishTicket(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    modName = models.CharField(max_length=100, default="", blank=True)
    userName = models.CharField(max_length=100, default="", null=True, blank=True)
    steamId = models.IntegerField(default=0, null=True, blank=True)
    punishment = models.CharField(max_length=10, null=True, blank=True, default="")
    banTime = models.CharField(max_length=10, null=True, blank=True, default="")
    banTimeOther = models.CharField(max_length=100, default="", null=True, blank=True)
    reason = models.TextField(max_length=1000, default="", null=True, blank=True)
    ticketLink = models.CharField(max_length=500, default="", null=True, blank=True)
    courtesy = models.BooleanField(default=False, blank=True)
    counterLink = models.CharField(max_length=500, default="", null=True, blank=True)
    discName = models.CharField(max_length=100, default="", null=True, blank=True)
    addtlMods = models.CharField(max_length=100, default="", blank=True, null=True)


class brokenRules(models.Model):
    user = models.ForeignKey(punishTicket, on_delete=models.CASCADE, related_name='brokenRules', null=True, blank=True)
    rules = models.CharField(max_length=6, null=True, blank=True)
    description = models.CharField(max_length=400, null=True, blank=True)
    clarity = models.TextField(max_length=2000, default="", blank=True)