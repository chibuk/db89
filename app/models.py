from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here

ADDERSS_MAX_LENGTH = 250
ITEM_NANME_MAX_LENGTH = 200
CITY_NAME_MAX_LENGTH = 50


class Item(models.Model):
    """
    Справочник товарных единиц, то, что заполняет табличную часть документа ТТН
    """
    name = models.CharField("Наименование", max_length=ITEM_NANME_MAX_LENGTH, help_text="Наименование", unique=True)

    class Meta:
        verbose_name = 'Наименование'
        verbose_name_plural = 'Наименования'

    def __str__(self):
        return self.name

    @staticmethod
    def get_absolute_url():
        return reverse('item-list') # kwargs={'pk': self.pk}


class City(models.Model):
    """
    Справочник городов
    """
    name = models.CharField("Город", max_length=CITY_NAME_MAX_LENGTH, help_text="Название города", unique=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

    def __str__(self):
        return self.name

    @staticmethod
    def get_absolute_url():
        return reverse('city-list') # kwargs={'pk': self.pk}


class Address(models.Model):
    """
    Справочник адресов
    """
    text = models.TextField("Введите адрес", help_text="Введите адрес", unique=True, max_length=ADDERSS_MAX_LENGTH)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.text


class Organization(models.Model):
    """
    Организации, справочник
    """
    name = models.CharField("Наименование организации", max_length=50, help_text='Название организации')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, verbose_name='Адрес', null=True)
    inn = models.CharField('ИНН', max_length=10, help_text='ИНН', blank=True)
    kpp = models.CharField('КПП', max_length=9, help_text='КПП', blank=True)
    ogrn = models.CharField('ОГРН', max_length=15, help_text='ОГРН или ОГРНИП', blank=True)
    bank = models.CharField('Банк, наименование', max_length=150, help_text='Наименование банка', blank=True)
    bik = models.CharField('БИК', max_length=9, help_text='БИК', blank=True)
    pay_acount = models.CharField('Расчетный счет', max_length=20, help_text='Расчетный счет', blank=True)
    kor_acount = models.CharField('Корр. счет', max_length=20, help_text='Корр. счет', blank=True)
    phone = models.CharField('Номера телефонов', max_length=40, help_text='Телефон', blank=True)
    email = models.EmailField('Адрес Email', help_text='Адрес email', blank=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return f'{self.name} {self.inn}'

#
# class RootOrganization(models.Model):
#     """ Корневая организация (владелец своей БД), от имени которой будут выписываться документы """
#     organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
#


class Document(models.Model):
    number = models.CharField("Номер", max_length=15, help_text='Номер документа', unique=True)
    data = models.DateField("Дата", auto_now_add=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация')
    city = models.ForeignKey(City, on_delete=models.PROTECT, help_text='Город', verbose_name='Город')
    truck = models.CharField("Номер ТС", max_length=20, help_text='№ ТС')
    sender = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True, null=True, related_name='doc_sender',
                               verbose_name='Отправитель')
    receiver = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True, null=True,
                                 related_name='doc_receiver', verbose_name='Получатель')
    payer = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True, null=True, related_name='doc_payer',
                              verbose_name='Плательщик')
    spec_notes = models.TextField("Особые отметки", help_text="Особые отметки", blank=True)
    destination_address = models.ForeignKey(Address, on_delete=models.PROTECT, blank=True,
                                            verbose_name='Адрес доставки')
    text = models.TextField("Условия договора", help_text='Условия договора', blank=True)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return f'{self.number} {self.data} {self.organization}'


class ItemsList(models.Model):
    """
    Строки табличной части документа ТТТН
    """
    document = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name='Документ')
    item = models.ForeignKey(Item, on_delete=models.PROTECT,
                             verbose_name="Наименование груза", help_text='Наименование')
    quantity = models.PositiveSmallIntegerField("Количество мест", help_text='Количество мест')
    weight = models.CharField("Вес", max_length=10, help_text='Вес', blank=True)
    volume = models.CharField("Объем", max_length=10, help_text='Объем', blank=True)
    price = models.CharField("Цена", max_length=10, help_text='Цена', blank=True)
    summ = models.PositiveIntegerField("Сумма", help_text='Сумма')

    class Meta:
        verbose_name = 'Строка'
        verbose_name_plural = 'Строки'

    def __str__(self):
        return f'{self.item.name} - {self.quantity} - {self.summ}'
