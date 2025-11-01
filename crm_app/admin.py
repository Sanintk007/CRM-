from django.contrib import admin
from .models import Company, Contact, Report


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


from django.contrib import admin
from .models import Company, Contact, Report

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'website')

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        obj.save()

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'user')

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        obj.save()

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at')

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        obj.save()
