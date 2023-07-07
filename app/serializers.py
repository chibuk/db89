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

    # sender = OrganizationSerializer()
    # receiver = OrganizationSerializer()
    # payer = OrganizationSerializer()