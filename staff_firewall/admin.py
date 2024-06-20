from django.contrib import admin
from django import forms
from .models import FwRegions, FwStaff


class FwRegionsAdminForm(forms.ModelForm):
    class Meta:
        model = FwRegions
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'api_key_encrypted' in self.changed_data:
            instance.api_key = self.cleaned_data['api_key_encrypted']
        if 'api_secret_encrypted' in self.changed_data:
            instance.api_secret = self.cleaned_data['api_secret_encrypted']
        if commit:
            instance.save()
        return instance


class FwRegionsAdmin(admin.ModelAdmin):
    form = FwRegionsAdminForm


admin.site.register(FwRegions, FwRegionsAdmin)
admin.site.register(FwStaff)
