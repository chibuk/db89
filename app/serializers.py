import re

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Organization, Document, DocumentItem, Item, ExtraInfo, RootOrganization, AppUser


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        exclude = ['root']
        # fields = '__all__'
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Organization.objects.all(),
        #         fields=['inn', 'root'],
        #         message='Организация с таким ИНН уже существует.'
        #     )
        # ]

    def validate_inn(self, value):
        if not re.match(r'[0-9]{10}', value):
            raise serializers.ValidationError("Неверный формат ИНН, должно быть 10 цифр.")
        return value

    # def validate_email(self, value):
    #     if not re.match(r"[A-z,-._]+@[A-z]+\.[A-z,-_.]{2,5}", value):
    #         raise serializers.ValidationError("Неверный формат адреса email.")
    #     return value


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


class ExtraInfoSerialiser(serializers.ModelSerializer):
    class Meta:
        model = ExtraInfo
        exclude = ['root']
        depth = 1

class AppUserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = '__all__'
        depth = 1


class RootOrganizationSerialiser(serializers.ModelSerializer):
    class Meta:
        model = RootOrganization
        fields = '__all__'
        depth = 1

#  Обратить  внимание:
#  CreateOnlyDefault
#  https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/overview/navigaciya-po-api/validators#rasshirennye-znacheniya-polei-po-umolchaniyu
#  https://www.django-rest-framework.org/api-guide/validators/#currentuserdefault