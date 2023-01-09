from django.contrib import admin

# Register your models here.
from .models import Address, City, Item, Organization, Document, ItemsList

admin.site.register(Address)
admin.site.register(City)
admin.site.register(Item)


class ItemsListAdmin(admin.ModelAdmin):
    list_display = ('document', 'item', 'quantity', 'price', 'summ')


admin.site.register(ItemsList, ItemsListAdmin)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'inn', 'phone', 'email')

admin.site.register(Organization, OrganizationAdmin)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('number', 'data', 'organization', 'city', 'destination_address')

admin.site.register(Document, DocumentAdmin)