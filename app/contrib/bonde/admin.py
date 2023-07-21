from django.contrib import admin

# Register your models here.
import admin2

from .models import Mobilization


admin2.site.register(Mobilization)