from django.contrib import admin
from .models import LogSession, Game, BaysianNet

# Register your models here.
admin.site.register(LogSession)
admin.site.register(Game)
admin.site.register(BaysianNet)