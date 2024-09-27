from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone




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
    phone_number = models.CharField(max_length=9, validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',  # Example regex for international phone numbers
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ])
    class Meta:
        db_table = 'Beneficiary'
    
class Station(models.Model):
    station_name = models.CharField(_("Station Name"), max_length=50)
    location = models.CharField(_("Station Location"), max_length=50)
    
    class Meta:
        db_table = 'Station'


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

class Supplier(models.Model):
    name = models.CharField(_("Full Name"), max_length=90, null=False)
    phone_number = models.CharField(max_length=9, validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',  # Example regex for international phone numbers
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ])
    class Meta:
        db_table = 'Supplier'
    
