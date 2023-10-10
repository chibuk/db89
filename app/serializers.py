from rest_framework import serializers
from .models import Organization, Document, DocumentItem, Item


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        exclude = ['root']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ['root']


class DocumentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentItem
        exclude = ['root']
        depth = 1


class DocumentSerializer(serializers.ModelSerializer):
    """Спсисок документоа"""
    class Meta:
        model = Document
        exclude = ['root']
        depth = 1

#  Обратить  внимание:
#  CreateOnlyDefault
#  https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/overview/navigaciya-po-api/validators#rasshirennye-znacheniya-polei-po-umolchaniyu
#  https://www.django-rest-framework.org/api-guide/validators/#currentuserdefault