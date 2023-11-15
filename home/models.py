from django.db import models

# Create your models here.
class Dino(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Strike(models.Model):
    strike = models.CharField(max_length=64)
    ban = models.BooleanField(default=False)

class Rule(models.Model):
    rule = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.rule

class Player(models.Model):
    discord_id = models.CharField(max_length=64)
    discord_name = models.CharField(max_length=64)
    game_name = models.CharField(max_length=64)
    steam_id = models.CharField(max_length=64)
    strike = models.IntegerField(default=0)
    
    
class PlayerAlt(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    alt_name = models.CharField(max_length=64)
    steam_id = models.CharField(max_length=64)

    def __str__(self):
        return self.alt_name

class ticket(models.Model):
    id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    players = models.ManyToManyField(Player)
    description = models.TextField()
    staff = models.CharField(max_length=64)
    transcript = models.TextField()
    status = models.CharField(max_length=64)
    appeal = models.TextField()

    def __str__(self):
        return self.id
    