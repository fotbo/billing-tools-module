from django.contrib import admin
from .models import FwRegions,FwDeviceType,FwActions,FwStaff

admin.site.register(FwRegions)
admin.site.register(FwDeviceType)
admin.site.register(FwActions)
admin.site.register(FwStaff)