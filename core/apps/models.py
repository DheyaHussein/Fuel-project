from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType





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

def generate_upload_path(instance, filename):
    if instance.content_type:
        return f'{instance.content_type.name}-images/{filename}'

class Image(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    image = models.ImageField(_("Image"), upload_to=generate_upload_path)
    # def save(self, *args, **kwargs):

    #     if self.content_type:
    #         self.image.upload_to = f'{self.content_type.name}/'
    #     return super().save(*args, **kwargs)
    def __str__(self):
        return self.image.url

CATEGORY_CHOICES = [
    ('gass', 'gass'),
    ('oil', 'oil'),
]

class Incoming(models.Model):
    # store_house = models.ForeignKey(StoreHouse, verbose_name=_("StoreHouse"), on_delete=models.CASCADE)
    store = models.ForeignKey(StoreHouse, verbose_name=_("StoreHouse"), on_delete=models.CASCADE)
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
    attach_file = GenericRelation(Image, related_query_name='attach_file')
    imported_quantites = models.CharField(_("imported quantites"), max_length=50)
    cat = models.CharField(_("catergory"), max_length=50, choices=CATEGORY_CHOICES)
    note = models.CharField(_("note"), max_length=50, blank=True)
    
    class Meta:
        db_table = 'Incoming'
        
    def __str__(self):
        return f'the incoming to  {self.store.name}  type of {self.cat}'
    
    def save(self, *args, **kwargs):
        # Convert imported_quantites to a numeric value
        if self.pk:  # If the object already exists (has been saved before)
            raise ValueError("This record cannot be modified after it's been saved.")
        try:
            imported_qty = float(self.imported_quantites)
        except ValueError:
            raise ValidationError(_("Imported quantities must be a valid number."))

        # Update the current_amount in the related StoreHouseCategroy
        store_categroy_qs = StoreHouseCategroy.objects.filter(storehouse=self.store, catergory__name=self.cat)
        

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
    attach_file = GenericRelation(Image, related_query_name='attach_file')
    outgoing_quantites = models.CharField(_("outgoing quantites"), max_length=50)
    cat = models.CharField(_("catergory"), max_length=50, choices=CATEGORY_CHOICES)
    note = models.CharField(_("note"), max_length=50)
    transfer_date = models.DateField(_("transfer date"), auto_now=False, auto_now_add=False)
    current_transfer_date = models.DateField(_("transfer date"), auto_now=False, auto_now_add=True)
    
    class Meta:
        db_table = 'Outgoing'
        
    def __str__(self):
        return f'the outgoing from  {self.store.name}  type of {self.cat}'

    
    
    def save(self, *args, **kwargs):
        if self.pk:
            raise ValueError("This record cannot be modified after it's been saved.")

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




class IncomingReturns(models.Model):
    incoming = models.ForeignKey(Incoming, verbose_name=_("Related Incoming"), on_delete=models.CASCADE)
    incoming_date = models.DateTimeField(_("Incoming Date"), editable=False)  # Derived from Incoming model
    store_house = models.ForeignKey(StoreHouse, verbose_name=_("Store House"), on_delete=models.CASCADE, editable=False)  # From Incoming
    supplier = models.ForeignKey(Supplier, verbose_name=_("Supplier"), on_delete=models.CASCADE, editable=False)  # From Incoming
    station = models.ForeignKey(Station, verbose_name=_("Station"), on_delete=models.CASCADE, editable=False)  # From Incoming
    paper_number = models.CharField(_("Numbering on Paper"), max_length=50, null=True)
    recipient_name = models.CharField(_("Recipient`s Name"), max_length=90, null=True)
    deliverer_name = models.CharField(max_length=50, null=True)
    recipient_miltry_number = models.CharField(max_length=50, null=True)
    deliverer_miltry_number = models.CharField(max_length=50, null=True)
    return_date = models.DateTimeField(_("Return Date"), auto_now=False, auto_now_add=True)
    cat = models.CharField(_("catergory"), max_length=50, choices=CATEGORY_CHOICES, null=True)
    returned_quantites = models.CharField(_("Returned Quantities"), max_length=50)
    reason_for_return = models.CharField(_("Reason for Return"), max_length=255)
    note = models.TextField(_("Additional Note"), blank=True, null=True)

    class Meta:
        verbose_name = _("Incoming Return")
        verbose_name_plural = _("Incoming Returns")
        db_table = 'IncomingReturns'

    def __str__(self):
        return f"Incoming Return of {self.returned_quantites} from {self.incoming}"

    def save(self, *args, **kwargs):
        # Set values from the related Incoming instance
        if self.incoming:
            self.incoming_date = self.incoming.incom_date
            self.store_house = self.incoming.store
            self.supplier = self.incoming.supplier
            self.station = self.incoming.station

        # Convert returned_quantites to a numeric value
        try:
            returned_qty = float(self.returned_quantites)
        except ValueError:
            raise ValidationError(_("Returned quantities must be a valid number."))

        # Find the StoreHouseCategroy based on the store_house and matching category (cat)
        if self.cat == self.incoming.cat:
            store_categroy_qs = StoreHouseCategroy.objects.filter(storehouse=self.store_house, catergory__name=self.incoming.cat)

        # Update the current_amount for matching storehouses and categories
        for store_categroy in store_categroy_qs:
            # Add returned quantities to the current amount
            if returned_qty < float(self.incoming.imported_quantites):  
              store_categroy.current_amount -= returned_qty
              store_categroy.save()
            else:
                raise ValidationError(_("the returned quantites it should not be biger then imported quantites"))

        super().save(*args, **kwargs)
 

class OutgoingReturns(models.Model):
    outgoing = models.ForeignKey(Outgoing, verbose_name=_("Related Outgoing"), on_delete=models.CASCADE)
    outgoing_date = models.DateTimeField(_("Outgoing Date"), editable=False)  # Derived from Outgoing model
    store_house = models.ForeignKey(StoreHouse, verbose_name=_("Store House"), on_delete=models.CASCADE, editable=False)  # From Outgoing
    supplier = models.ForeignKey(Supplier, verbose_name=_("Supplier"), on_delete=models.CASCADE, editable=False)  # From Outgoing
    paper_number = models.CharField(_("Numbering on Paper"), max_length=50)
    recipient_name = models.CharField(_("Recipient`s Name"), max_length=90)
    deliverer_name = models.CharField(max_length=50)
    recipient_miltry_number = models.CharField(max_length=50)
    deliverer_miltry_number = models.CharField(max_length=50)
    return_date = models.DateTimeField(_("Return Date"), auto_now=False, auto_now_add=True)
    beneficiary = models.CharField(_("beneficiary"), max_length=50, editable=False)
    cat = models.CharField(_("catergory"), max_length=50, choices=CATEGORY_CHOICES, null=True)
    returned_quantites = models.CharField(_("Returned Quantities"), max_length=50)
    reason_for_return = models.CharField(_("Reason for Return"), max_length=255)
    note = models.TextField(_("Additional Note"), blank=True, null=True)

    class Meta:
        verbose_name = _("Outgoing Return")
        verbose_name_plural = _("Outgoing Returns")
        db_table = 'OutgoingReturns'

    def __str__(self):
        return f"Outgoing Return of {self.returned_quantites} from {self.outgoing}"    
    def save(self, *args, **kwargs):
        if self.outgoing:
            self.outgoing_date = self.outgoing.outging_date
            self.store_house = self.outgoing.store_house
            self.beneficiary = self.outgoing.beneficiary
        try:
            returned_qty = float(self.returned_quantites)
        except ValueError:
            raise  ValidationError(_("Returned quantities must be a valid number."))
        
        
        if self.cat == self.outgoing.cat:
            store_categroy_qs = StoreHouseCategroy.objects.filter(storehouse=self.store_house, catergory__name=self.outgoing.cat)
        
        for store_categroy in store_categroy_qs:
            if returned_qty < float(self.outgoing.outgoing_quantites):
                store_categroy.current_amount += self.returned_quantites
            else:
                raise ValidationError(_("the returned quantites it should not be biger then outgoing quantites"))
                
class Damaged(models.Model):
    store = models.ForeignKey(StoreHouse, verbose_name=_("StoreHouse"), on_delete=models.CASCADE)
    damaged_date = models.DateField(_("damaged date"), auto_now=False, auto_now_add=False)
    paper_number = models.CharField(_("Numbering on Paper"), max_length=50)
    recipient_name = models.CharField(_("Recipient`s Name"), max_length=90)
    recipient_miltry_number = models.CharField(max_length=50)
    deliverer_name = models.CharField(max_length=50)
    deliverer_miltry_number = models.CharField(max_length=50)
    damaged_quantites = models.FloatField(_("Damaged Quantities"))
    cat = models.CharField(_("catergory"), max_length=50, choices=CATEGORY_CHOICES)
    reason_for_damaged = models.CharField(_("Reason for Damaged"), max_length=255)
    note = models.TextField(_("Additional Note"), blank=True, null=True)
    
    class Meta:
        db_table = 'Damaged'
     
    def save(self, *args, **kwargs):
        
        store_categroy_qs = StoreHouseCategroy.objects.filter(storehouse=self.store, catergory__name=self.cat)
        for store_amount in store_categroy_qs:
            store_amount.current_amount -= self.damaged_quantites
            store_amount.save()
            
        super().save(*args, **kwargs)
        
 
class TransformationStoreHouse(models.Model):
    from_storehouse = models.ForeignKey(StoreHouse, related_name='transfer_from', verbose_name=_("Transform from"), on_delete=models.CASCADE)
    to_storehouse = models.ForeignKey(StoreHouse, related_name='transfer_to', verbose_name=_("Transform to"), on_delete=models.CASCADE)
    transform_date = models.DateField(_("Transfor date"), auto_now=False, auto_now_add=False)
    paper_number = models.CharField(_("Numbering on Paper"), max_length=50)
    recipient_name = models.CharField(_("Recipient`s Name"), max_length=90)
    recipient_miltry_number = models.CharField(max_length=50)
    deliverer_name = models.CharField(max_length=50)
    deliverer_miltry_number = models.CharField(max_length=50)
    transform_quantites = models.FloatField(_("Transform Quantities"))
    reason_for_transform = models.CharField(_("Reason for Return"), max_length=255)
    cat = models.CharField(_("catergory"), max_length=50, choices=CATEGORY_CHOICES, null=True)
    note = models.TextField(_("Additional Note"), blank=True, null=True)
    
    
 
     
 
    class Meta:
         verbose_name = _("transformationStoreHouse")
         verbose_name_plural = _("transformationStoreHouses")
         db_table = 'TransformationStoreHouse'
 
    def __str__(self):
         return f'Transform from {self.from_storehouse} to {self.to_storehouse}'
 
    #  def get_absolute_url(self):
    #      return reverse("transformationStoreHouse_detail", kwargs={"pk": self.pk})
    def save(self, *args, **kwargs):
        # Fetch StoreHouseCategory records for 'from_storehouse' and 'to_storehouse'
        store_category_from = StoreHouseCategroy.objects.filter(storehouse=self.from_storehouse, catergory__name=self.cat).first()
        store_category_to = StoreHouseCategroy.objects.filter(storehouse=self.to_storehouse, catergory__name=self.cat).first()
        print(store_category_from)

        # Check if there's enough stock in the from_storehouse
        if store_category_from and store_category_to:
            if self.transform_quantites <= store_category_from.current_amount:
                # Subtract quantity from 'from_storehouse'
                store_category_from.current_amount -= self.transform_quantites
                store_category_from.save()

                # Add quantity to 'to_storehouse'
                store_category_to.current_amount += self.transform_quantites
                store_category_to.save()
            else:
                raise ValidationError(_("The transform quantities must not exceed the available quantity in the 'from' store."))
        else:
            raise ValidationError(_("Either the 'from' storehouse or 'to' storehouse category does not exist."))

        # Call the parent save method
        super().save(*args, **kwargs)
            
        
        
               
               