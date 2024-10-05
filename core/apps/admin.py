from django.contrib import admin

# Register your models here.
from .models import Category, StoreHouseType, StoreHouse, Outgoing, Incoming, Station, Supplier, StoreHouseCategroy, Beneficiary, IncomingReturns

# ModelAdmin for Category
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
    list_display = ('incom_date', 'paper_number', 'supplier', 'station', 'supply_voucher_number', 'recipient_name', 'deliverer_name', 'imported_quantites', 'cat', 'note')
    
    # Fields to enable search functionality
    search_fields = ('store_house__storehouse__name', 'paper_number', 'recipient_name', 'deliverer_name', 'imported_quantites', 'cat', 'note')
    
    # Ordering the list by incoming date
    ordering = ('incom_date',)
    
    # Option to filter by store house, supplier, and station
    list_filter = ('store', 'supplier', 'station')

# ModelAdmin for Outgoing
class OutgoingAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('store_house', 'outging_date', 'paper_number', 'beneficiary', 'supply_voucher_number', 'recipient_name', 'deliverer_name', 'outgoing_quantites', 'cat', 'note', 'transfer_date', 'current_transfer_date')
    
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
    list_display = ('incoming', 'incoming_date', 'store_house', 'supplier', 'station', 'return_date', 'returned_quantites')
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