from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here
class Organization(models.Model):
    """
    Организации, справочник
    """
    name = models.CharField("Наименование организации", max_length=50, help_text='Название организации')
    address = models.CharField('Адрес', max_length=256, blank=True, help_text="Адрес")
    inn = models.CharField('ИНН', max_length=10, help_text='ИНН', blank=True)
    kpp = models.CharField('КПП', max_length=9, help_text='КПП', blank=True)
    ogrn = models.CharField('ОГРН', max_length=15, help_text='ОГРН или ОГРНИП', blank=True)
    bank = models.CharField('Банк, наименование', max_length=150, help_text='Наименование банка', blank=True)
    bik = models.CharField('БИК', max_length=9, help_text='БИК', blank=True)
    pay_acount = models.CharField('Расчетный счет', max_length=20, help_text='Расчетный счет', blank=True)
    kor_acount = models.CharField('Корр. счет', max_length=20, help_text='Корр. счет', blank=True)
    phone = models.CharField('Номера телефонов', max_length=40, help_text='Телефон', blank=True)
    email = models.EmailField('Адрес Email', help_text='Адрес email', blank=True)
    root = models.ForeignKey('RootOrganization',
                             on_delete=models.CASCADE,
                             help_text="Профиль",
                             verbose_name="Профиль",
                             null=True,
                             blank=True,
                             default=None)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} {self.inn}'

    def get_absolute_url(self):
        return reverse('organization-detail', kwargs={'pk': self.pk})


class AppUser(models.Model):
    """ Расширенный "пользователь", чтобы хранить ссылку на текущую RootOrganization """
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name="Пользователь",
                                help_text="Пользователь")
    root_organization = models.ForeignKey("RootOrganization",
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          blank=True,
                                          default=None,
                                          verbose_name="Профиль",
                                          help_text="Профиль")

    class Meta:
        verbose_name = 'Пользователь БД'
        verbose_name_plural = 'Пользователи БД'
        ordering = ['user']

    def get_absolute_url(self):
        return reverse('appuser-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.user.get_username()} ({self.user.get_full_name()})"


class RootOrganization(models.Model):
    """ Корневая организация (владелец своей БД), от имени которой будут выписываться документы """
    profile = models.OneToOneField(Organization,
                                   on_delete=models.RESTRICT,
                                   verbose_name='Организация (профиль)',
                                   help_text='Организация (профиль)',
                                   unique=True)

    users = models.ManyToManyField(AppUser,
                                    verbose_name='Пользователи',
                                    help_text='Пользователи',
                                    blank=True)

    class Meta:
        verbose_name = 'Организация-профиль'
        verbose_name_plural = 'Организации-профиль'
        ordering = ['profile']

    def get_absolute_url(self):
        return reverse('rootorganization-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.profile.name


class Item(models.Model):
    """
    Справочник товарных единиц (наименование груза), то, что заполняет табличную часть документа ТТН
    """
    name = models.CharField("Наименование груза", max_length=128, help_text="Наименование", unique=False, blank=False)
    root = models.ForeignKey('RootOrganization',
                             on_delete=models.CASCADE,
                             help_text="Профиль",
                             verbose_name="Профиль")

    class Meta:
        verbose_name = 'Наименование груза'
        verbose_name_plural = 'Наименования груза'
        # ordering = ['name'] # это ресурсозатратно
        # Уникальность name для root (same as unique_together):
        constraints = [
            models.UniqueConstraint(fields=['name', 'root'], name='root_name_uinique')
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})


class Document(models.Model):
    number = models.CharField("Номер", max_length=15, help_text='Номер документа', unique=True)
    data = models.DateField("Дата", auto_now_add=True)
    root = models.ForeignKey(RootOrganization,
                             on_delete=models.CASCADE,
                             help_text="Профиль",
                             verbose_name='Профиль')
    city = models.CharField('Город', max_length=100, help_text='Город')
    truck = models.CharField("Номер ТС", max_length=20, help_text='№ ТС')
    sender = models.ForeignKey(Organization,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True,
                               related_name='doc_sender',
                               verbose_name='Отправитель')
    receiver = models.ForeignKey(Organization,
                                 on_delete=models.PROTECT,
                                 blank=True,
                                 null=True,
                                 related_name='doc_receiver',
                                 verbose_name='Получатель')
    payer = models.ForeignKey(Organization,
                              on_delete=models.PROTECT,
                              blank=True,
                              null=True,
                              related_name='doc_payer',
                              verbose_name='Плательщик')
    spec_notes = models.TextField("Особые отметки", help_text="Особые отметки", blank=True)
    destination_address = models.CharField("Адрес доставки", max_length=256, help_text='Адрес доставки', blank=True)
    text = models.TextField("Условия договора", help_text='Условия договора', blank=True)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['number']

    def __str__(self):
        return f'{self.root} - {self.number} {self.data}'

    def get_absolute_url(self):
        return reverse('document-detail', kwargs={'pk': self.pk})


class DocumentItem(models.Model):
    item = models.ForeignKey(Item,
                             on_delete=models.PROTECT,
                             help_text='Строка в таблице документа',
                             verbose_name='Груз')
    document = models.ForeignKey(Document,
                                 on_delete=models.CASCADE,
                                 help_text='Документ',
                                 verbose_name='Документ',
                                 related_name='items')
    weight = models.CharField("Вес", max_length=25, help_text="Вес", blank=True)
    volume = models.CharField("Объём", max_length=25, help_text="Объём", blank=True)
    price = models.DecimalField("Цена", max_digits=14, decimal_places=2, help_text="Цена")
    seats = models.PositiveSmallIntegerField('Количество мест', help_text='Количество мест')
    root = models.ForeignKey(RootOrganization,
                             on_delete=models.CASCADE,
                             help_text="Профиль",
                             verbose_name='Профиль')

    class Meta:
        verbose_name = 'Груз'
        verbose_name_plural = 'Строки груза'
        ordering = ['item']

    def __str__(self):
        return f'{self.item} - {self.document} {self.seats}'

    @property
    def summ(self):
        return self.seats * self.price
