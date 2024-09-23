from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Category(models.Model):

    name = models.CharField(_("name"), max_length=100)
    

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categorys")
        db_table = 'Catgeroy'

    def __str__(self):
        return self.name


class StoreHouseType(models.Model):

    catergory = models.ForeignKey(Category, verbose_name=_("category"), on_delete=models.CASCADE)
    measurement_type = models.CharField(_("measurement_type"), max_length=50)
    opening_balance = models.FloatField(_("open_balance"))
    current_amount = models.FloatField(_("amount"))
    

    class Meta:
        verbose_name = _("StoreHouseType")
        verbose_name_plural = _("StoreHouseTypes")
        db_table = 'StoreHouseType'

    def __str__(self):
        return self.catergory.name


class StoreHouse(models.Model):
    name = models.CharField(_("name"), max_length=50)
    store_categroy = models.ForeignKey(StoreHouseType, verbose_name=_("StoreHouseType"), on_delete=models.CASCADE)
    storekeeper = models.CharField(_("Storekeeper"), max_length=100)
    phone_number = models.CharField(_("phone_number"), max_length=30)
    location = models.CharField(_("Location"), max_length=90)
    

    class Meta:
        verbose_name = _("StoreHouse")
        verbose_name_plural = _("StoreHouses")
        db_table = 'StoreHouse'

    def __str__(self):
        return self.name


