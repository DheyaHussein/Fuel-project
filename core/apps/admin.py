from django.contrib import admin

# Register your models here.
from .models import Category, StoreHouseType, StoreHouse

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
    list_display = ('name', 'store_categroy', 'storekeeper', 'phone_number', 'location')
    
    # Fields to enable search functionality
    search_fields = ('name', 'storekeeper', 'phone_number', 'location')
    
    # Ordering the list by name
    ordering = ('name',)
    
    # Option to filter by store category and location
    list_filter = ('store_categroy', 'location')

# Registering all models with their respective ModelAdmin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(StoreHouseType, StoreHouseTypeAdmin)
admin.site.register(StoreHouse, StoreHouseAdmin)