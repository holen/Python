from django.contrib import admin
from op.models import Machine, Load

# Register your models here.
class MachineAdmin(admin.ModelAdmin):
    #list_display = ('machine_name', 'machine_ip', 'machine_user', 'machine_passwd', 'machine_update_time')
    #list_display = ('machine_name', 'machine_ip', 'machine_user', 'machine_passwd')
    list_filter = ['machine_ip']
    search_fields = ['machine_name']

class LoadAdmin(admin.ModelAdmin):
    #list_display = ('load_id', 'load_ip', 'load_server', 'load_str', 'load_ip_count', 'load_update_time')
    list_display = ('load_id', 'load_ip', 'load_server', 'load_str', 'load_ip_count')
    list_filter = ['load_ip']
    search_fields = ['load_id']

admin.site.register(Machine, MachineAdmin)
admin.site.register(Load, LoadAdmin)
