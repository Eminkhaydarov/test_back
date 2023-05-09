from django.contrib import admin

from .models import MenuItem, Menu


# Register your models here.
class ItemInline(admin.StackedInline):
    model = MenuItem
    extra = 5


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    inlines = [ItemInline]


admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Menu)