from django.contrib import admin

# Register your models here.
from app.models import Item, Organization, Document, AppUser, RootOrganization, DocumentItem


class AppUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'root_organization')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'root')


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'inn', 'phone', 'email', 'root')


class DocumentItemAdmin(admin.TabularInline):
    model = DocumentItem
    list_display = ('document', 'item', 'weight', 'volume', 'price', 'seats', 'root')


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('number', 'data', 'root', 'city', 'destination_address')
    inlines = [DocumentItemAdmin]


admin.site.register(Document, DocumentAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(RootOrganization)
admin.site.register(AppUser, AppUserAdmin)
