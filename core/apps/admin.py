from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.contenttypes.admin import GenericTabularInline
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
    ReadOnlyPasswordHashField,
    UsernameField,
)  # Register your models here.



# ModelAdmin for Category

class CustomUserChangeForm(forms.ModelForm):
    """
    Custom UserChangForm For AdminUser registertions
    """
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = ("name", "email", "is_active", "is_staff",
                  "is_superuser",  "groups", "username",)
        # field_classes = {"email": forms.EmailField}


class CustomUserCreationForm(UserCreationForm):
    """
        Custom UserChangForm For AdminUser registertions
    """
    class Meta:
        model = User
        fields = ("name", "email", "is_active", "is_staff",
                  "is_superuser",  "groups", "username",)
        # field_classes = {'email': forms.EmailField}


class CustomAdminUser(UserAdmin):
    """
        Custom CustomUSerAdmin For User registertions to add grops and Custom Disgan

    """
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {
         "fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "user_type"
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", 'name', "user_type"),
            },
        ),
    )
    form = CustomUserChangeForm

    def save_model(self, request, obj, form, change):
        # Save the user object in Django database
        obj.save()

        # # Check if the user is newly created (not updated)
        # if not change:
        #     # Add the user to Firebase
        #     db = firestore.client()
        #     users_ref = db.collection('Users')
        #     users_ref.document(str(obj.id)).set({
        #         'email': obj.email,
        #         'fullName': obj.name,
        #         'userType': obj.user_type,
        #         'phone_number': obj.phone_number,
        #         'imageUrl': obj.image.url if obj.image else '',
        #         # Add other fields as needed
        #     }, merge=True)

    # add_form = CustomUserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("email", "name",
                     "is_staff", 'is_deleted', 'is_active')
    list_filter = ("is_staff", "is_superuser",
                   "is_active", "groups",  'is_deleted', 'is_active')
    search_fields = ("username",
                     "phone_number", "name", "email")
    ordering = ("id",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def get_queryset(self, request):

        qs = self.model._default_manager.get_queryset()
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.all()
        return qs









class ImageInline(GenericTabularInline):
    model = Image
    extra = 1  # Number of extra forms to display 

class CategoryAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('name',)
    
    # Fields to enable search functionality
    search_fields = ('name',)
    
    # Order the results in the list view by name
    ordering = ('name',)
    
    # Option to filter by name in the admin
    list_filter = ('name',)

# ModelAdmin for StoreHouseType
class StoreHouseTypeAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('catergory', 'measurement_type', 'opening_balance', 'current_amount')
    
    # Fields to enable search functionality
    search_fields = ('catergory__name', 'measurement_type')
    
    # Ordering the list by category and measurement type
    ordering = ('catergory', 'measurement_type')
    
    # Option to filter by category and measurement type
    list_filter = ('catergory', 'measurement_type')

# ModelAdmin for StoreHouse
class StoreHouseAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('name', 'storekeeper', 'phone_number', 'location')
    
    # Fields to enable search functionality
    search_fields = ('name', 'storekeeper', 'phone_number', 'location')
    
    # Ordering the list by name
    ordering = ('name',)
    
    # Option to filter by store category and location
    # list_filter = ('location')
    
    # Custom method to display current_amount from related StoreHouseType
    # def current_amount(self, obj):
    #     return obj.store_categroy
    
    # # Set a readable name for the custom column
    # current_amount.short_description = 'Current Amount'
    
class StoreHouseCategroyAdmin(admin.ModelAdmin):
    list_display = ('catergory', 'storehouse', 'measurement_type', 'opening_balance', 'current_amount')
        
    
class IncomingAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    inlines = [ImageInline]  # Add Image inline

    list_display = ('incom_date', 'paper_number', 
                    'supplier', 'station', 'supply_voucher_number', 'recipient_name',
                    'deliverer_name', 'imported_quantites', 'cat', 'note')
    
    # Fields to enable search functionality
    search_fields = ('store_house__storehouse__name', 'paper_number', 'recipient_name',
                     'deliverer_name', 'imported_quantites', 'cat', 'note')
    
    # Ordering the list by incoming date
    ordering = ('incom_date',)
    
    # Option to filter by store house, supplier, and station
    list_filter = ('store', 'supplier', 'station')

# ModelAdmin for Outgoing
class OutgoingAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    inlines = [ImageInline]  # Add Image inline

    list_display = ('store_house', 'outging_date', 'paper_number', 'beneficiary',
                    'supply_voucher_number', 'recipient_name', 'deliverer_name',
                    'outgoing_quantites', 'cat', 'note', 'transfer_date', 'current_transfer_date')
    
    # Fields to enable search functionality
    search_fields = ('store_house__name', 'paper_number', 'recipient_name', 'deliverer_name', 'outgoing_quantites', 'cat', 'note')
    
    # Ordering the list by outgoing date
    ordering = ('outging_date',)
    
    # Option to filter by store house, beneficiary, and transfer dates
    list_filter = ('store_house', 'beneficiary', 'transfer_date', 'current_transfer_date')



class SupplierAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('name', 'phone_number')
    
    # Fields to enable search functionality
    search_fields = ('name', 'phone_number')
    
    # Ordering the list by supplier's name
    ordering = ('name',)
    
    # Option to filter by name
    list_filter = ('name',)

# ModelAdmin for Station
class StationAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('station_name', 'location')
    
    # Fields to enable search functionality
    search_fields = ('station_name', 'location')
    
    # Ordering the list by station name
    ordering = ('station_name',)
    
    # Option to filter by station name and location
    list_filter = ('station_name', 'location')


class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number')
    
    


class IncomingReturnsAdmin(admin.ModelAdmin):
    list_display = ('incoming', 'incoming_date', 'store_house', 'supplier', 'station', 'return_date', 'cat',  'returned_quantites')
    search_fields = ('incoming__paper_number', 'supplier__name', 'store_house__name', 'station__station_name')
    list_filter = ('incoming_date', 'store_house', 'supplier', 'station')
    readonly_fields = ('incoming_date', 'store_house', 'supplier', 'station')

    def has_add_permission(self, request):
        # Allow add permission only if there is a related Incoming record
        return Incoming.objects.exists()

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class OutgoingReturnsAdmin(admin.ModelAdmin):
    list_display = ('outgoing', 'outgoing_date', 'store_house', 'supplier', 'paper_number', 'recipient_name', 'deliverer_name', 'returned_quantites', 'return_date')
    search_fields = ('outgoing__paper_number', 'supplier__name', 'store_house__name', 'recipient_name')
    list_filter = ('outgoing_date', 'store_house', 'supplier')
    readonly_fields = ('outgoing_date', 'store_house', 'supplier', 'beneficiary')

    def has_add_permission(self, request):
        # Ensure that new returns can only be added if there are outgoing records
        return Outgoing.objects.exists()



class TransformationStoreHouseAdmin(admin.ModelAdmin):
    list_display = ('from_storehouse', 'to_storehouse', 'transform_date', 'paper_number', 'recipient_name', 'deliverer_name', 'transform_quantites', 'cat')
    search_fields = ('from_storehouse__name', 'to_storehouse__name', 'paper_number', 'recipient_name', 'deliverer_name', 'cat')
    list_filter = ('transform_date', 'from_storehouse', 'to_storehouse', 'cat')
    # readonly_fields = ('from_storehouse', 'to_storehouse', 'transform_date')

    def has_add_permission(self, request):
        # Allow adding transformations only if there are storehouses
        return StoreHouse.objects.exists()
    def save_model(self, request, obj, form, change):
        # Check if this is a new instance (not yet saved)
        if not change:  # Only apply logic on create
            store_category_from = StoreHouseCategroy.objects.filter(storehouse=obj.from_storehouse, catergory__name=obj.cat).first()
            store_category_to = StoreHouseCategroy.objects.filter(storehouse=obj.to_storehouse, catergory__name=obj.cat).first()

            if store_category_from and store_category_to:
                if obj.transform_quantites <= store_category_from.current_amount:
                    # Adjust quantities directly
                    store_category_from.current_amount -= obj.transform_quantites
                    store_category_from.save()
                    
                    store_category_to.current_amount += obj.transform_quantites
                    store_category_to.save()
                else:
                    raise ValidationError(_("The transform quantities must not exceed the available quantity in the 'from' store."))
            else:
                raise ValidationError(_("Either the 'from' storehouse or 'to' storehouse category does not exist."))

        # Save the instance without triggering `save` logic in the model
        super().save_model(request, obj, form, change)




class DamagedAdmin(admin.ModelAdmin):
    list_display = ('store', 'damaged_date', 'paper_number', 'recipient_name', 'deliverer_name', 'damaged_quantites', 'cat', 'reason_for_damaged')
    search_fields = ('store__name', 'paper_number', 'recipient_name', 'deliverer_name', 'cat')
    list_filter = ('damaged_date', 'store', 'cat')
    readonly_fields = ('damaged_date', 'store', 'paper_number')

    def has_add_permission(self, request):
        # Check if there are any stores available for damaged items
        return StoreHouse.objects.exists()


admin.site.register(User, CustomAdminUser)
admin.site.register(TransformationStoreHouse, TransformationStoreHouseAdmin)
admin.site.register(Damaged, DamagedAdmin)
admin.site.register(OutgoingReturns, OutgoingReturnsAdmin)    
admin.site.register(IncomingReturns, IncomingReturnsAdmin)
admin.site.register(Beneficiary, BeneficiaryAdmin)
admin.site.register(Incoming, IncomingAdmin)
admin.site.register(Outgoing, OutgoingAdmin)
admin.site.register(StoreHouseCategroy, StoreHouseCategroyAdmin)

# Registering all models with their respective ModelAdmin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(StoreHouseType, StoreHouseTypeAdmin)
admin.site.register(StoreHouse, StoreHouseAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Station, StationAdmin)