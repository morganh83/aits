from django.contrib import admin

# Register your models here.


from .models import dinoName, strikeType, banLength, Rule

admin.site.register(dinoName)
admin.site.register(strikeType)
admin.site.register(banLength)
admin.site.register(Rule)
