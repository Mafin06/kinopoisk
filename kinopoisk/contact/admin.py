from django.contrib import admin

from .models import Contact

# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "date")
    list_filter = ("date",)
    search_fields = ("email",)
    date_hierarchy = "date"