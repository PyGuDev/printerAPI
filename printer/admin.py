from django.contrib import admin
from .models import Printer, Check


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'check_type', 'point_id', 'api_key')
    list_filter = ('check_type', 'point_id')


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('printer_id', 'type', 'order', 'status')
    list_filter = ('printer_id', 'type', 'status')