from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError






# Create your models here.



class MyUserManager(BaseUserManager):
    """
    Custom User Manager
    """

    def _create_user(self,  email, username,  password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        # GlobalUserModel = apps.get_model(
        #     self.model._meta.app_label, self.model._meta.object_name
        # )
        # username = GlobalUserModel.normalize_username(username)
        user = self.model(email=email,  username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username=None,  password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, username, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    
    
    user_type_choices = [
        ("manager", "StoreHouse Manager"),
        ("employee", "StoreHouse Employee"),
    ]
    
    name = models.CharField(_("Full Name"), max_length=50)
    username = models.CharField(_("User name"), max_length=50,
                                null=True,
                                help_text=_(
                                    "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
                                ),
                                blank=True,
                                error_messages={
                                     "unique": _("A user with that username already exists."),

                                }
                            )
    user_type = models.CharField(_("User Type"), max_length=50, choices=user_type_choices, default="employee")
    email = models.EmailField(_("email address"), max_length=254, unique=True)
    register_data = models.CharField(max_length=20, default='')
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_deleted = models.BooleanField(_('Deleted'), default=False,)
    date_joined = models.DateTimeField(
        _("date joined"),  default=timezone.now, )
    
    objects = MyUserManager()
    USERNAME_FIELD = "email"
    
    def get_full_name(self):
        full_name = "%s " % (self.name)
        return full_name
    
    def save(self, *args, **kwargs):
        # if not self.id:
        return super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'User'
            
    
    
class Beneficiary(models.Model):
    name = models.CharField(_("Full Name"), max_length=50)
    phone_number = models.CharField(max_length=9)
    class Meta:
        db_table = 'Beneficiary'
    def __str__(self):
        return self.name
    
class Station(models.Model):
    station_name = models.CharField(_("Station Name"), max_length=50)
    location = models.CharField(_("Station Location"), max_length=50)
    
    class Meta:
        db_table = 'Station'
    def __str__(self):
        return self.station_name


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
    # store_categroy = models.ForeignKey(StoreHouseType, verbose_name=_("StoreHouseType"), on_delete=models.CASCADE)
    # store_categroy = models.ManyToManyField(StoreHouseType)

    
    storekeeper = models.CharField(_("Storekeeper"), max_length=100)
    phone_number = models.CharField(_("phone_number"), max_length=30)
    location = models.CharField(_("Location"), max_length=90)
    

    class Meta:
        verbose_name = _("StoreHouse")
        verbose_name_plural = _("StoreHouses")
        db_table = 'StoreHouse'

    def __str__(self):
        return self.name
    
class StoreHouseCategroy(models.Model):
    
    catergory = models.ForeignKey(Category, verbose_name=_("category"), on_delete=models.CASCADE)
    storehouse = models.ForeignKey(StoreHouse, verbose_name=_("storehouse"), on_delete=models.CASCADE)
    measurement_type = models.CharField(_("measurement_type"), max_length=50)
    opening_balance = models.FloatField(_("open_balance"))
    current_amount = models.FloatField(_("amount"))
    

    class Meta:
        verbose_name = _("StoreHouseCategroy")
        verbose_name_plural = _("StoreHouseCategroy")
        db_table = 'StoreHouseCategroy'
        constraints = [
            models.UniqueConstraint(fields=['catergory', 'storehouse'], name='unique_catergory_storehouse')
        ]

    def __str__(self):
        return self.storehouse.name
    

class Supplier(models.Model):
    name = models.CharField(_("Full Name"), max_length=90, null=False)
    phone_number = models.CharField(max_length=9)
    class Meta:
        db_table = 'Supplier'
        
    def __str__(self):
        return self.name

# def generate_upload_to_path(instance, filename):
#     if instance.content_type:
#         return f'{instance.content_type.name}-images/{filename}'
#     return f'images/unknown/{filename}'


# class Image(models.Model):

#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey()
#     image = models.ImageField(_("Image"), upload_to=generate_upload_to_path)
#     # def save(self, *args, **kwargs):

#     #     if self.content_type:
#     #         self.image.upload_to = f'{self.content_type.name}/'
#     #     return super().save(*args, **kwargs)
#     def __str__(self):
#         return self.image.url



class Incoming(models.Model):
    # store_house = models.ForeignKey(StoreHouse, verbose_name=_("StoreHouse"), on_delete=models.CASCADE)
    store = models.ForeignKey(StoreHouseCategroy, verbose_name=_("StoreHouse"), on_delete=models.CASCADE)
    incom_date = models.DateTimeField(_("incom_date"), auto_now=False, auto_now_add=False)
    paper_number = models.CharField(_("Numbering on Paper"), max_length=50)
    supplier = models.ForeignKey(Supplier, verbose_name=_("Supplier"), on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    supply_voucher_number = models.CharField(max_length=50)
    recipient_name = models.CharField(_("Recipient`s Name"), max_length=90)
    deliverer_name = models.CharField(max_length=50)
    recipient_miltry_number = models.CharField(max_length=50)
    deliverer_miltry_number = models.CharField(max_length=50)
    # statement = models.CharField(_("statement"), max_length=50)
    # attach_file = GenericRelation(Image, related_query_name='attach_file')
    imported_quantites = models.CharField(_("imported quantites"), max_length=50)
    cat = models.CharField(_("catergory"), max_length=50)
    note = models.CharField(_("note"), max_length=50)
    
    class Meta:
        db_table = 'Incoming'
        
    def __str__(self):
        return self.store.storehouse.name
    
    def save(self, *args, **kwargs):
        # Convert imported_quantites to a numeric value
        try:
            imported_qty = float(self.imported_quantites)
        except ValueError:
            raise ValidationError(_("Imported quantities must be a valid number."))

        # Update the current_amount in the related StoreHouseCategroy
        store_categroy_qs = StoreHouseCategroy.objects.filter(catergory__name=self.cat)

        # Update the current_amount for matching categories
        for store_categroy in store_categroy_qs:
            store_categroy.current_amount += imported_qty
            store_categroy.save()

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'Incoming'
    
    
    

class Outgoing(models.Model):
    store_house = models.ForeignKey(StoreHouse, verbose_name=_("StoreHouse"), on_delete=models.CASCADE)
    outging_date = models.DateTimeField(_("outging date"), auto_now=False, auto_now_add=True)
    paper_number = models.CharField(_("Numbering on Paper"), max_length=50)
    beneficiary = models.ForeignKey(Beneficiary, verbose_name=_("Beneficiary"), on_delete=models.CASCADE)
    supply_voucher_number = models.CharField(max_length=50)
    recipient_name = models.CharField(_("Recipient`s Name"), max_length=90)
    deliverer_name = models.CharField(max_length=50)
    recipient_miltry_number = models.CharField(max_length=50)
    deliverer_miltry_number = models.CharField(max_length=50)
    # statement = models.CharField(_("statement"), max_length=50)
    # attach_file = GenericRelation(Image, related_query_name='attach_file')
    outgoing_quantites = models.CharField(_("outgoing quantites"), max_length=50)
    cat = models.CharField(_("catergory"), max_length=50)
    note = models.CharField(_("note"), max_length=50)
    transfer_date = models.DateField(_("transfer date"), auto_now=False, auto_now_add=False)
    current_transfer_date = models.DateField(_("transfer date"), auto_now=False, auto_now_add=True)
    
    class Meta:
        db_table = 'Outgoing'
        
    def __str__(self):
        return self.store_house.name
    
    
    def save(self, *args, **kwargs):
        outgogin_qty = float(self.outgoing_quantites)
        storehouse_type = self.store_house.id
        print(storehouse_type)
        
        store_categroy_qs = StoreHouseCategroy.objects.filter(storehouse=self.store_house, catergory__name=self.cat)
        print(store_categroy_qs)
        for stor in store_categroy_qs:
            if stor.current_amount < outgogin_qty:
                raise ValidationError(_("Not enough stock in the storehouse for this category."))  
              
            
            stor.current_amount -= outgogin_qty
            print(stor.current_amount)
            stor.save()
        
        
        # Update the current_amount of StoreHouseType
        # storehouse_type.current_amount -= outgogin_qty
        # storehouse_type.save()
        
        # Call the original save method to save the Incoming object
        super().save(*args, **kwargs)



 
    
    
      
      
    
    
    
