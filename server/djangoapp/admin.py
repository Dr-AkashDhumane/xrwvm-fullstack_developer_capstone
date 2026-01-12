from django.contrib import admin
from .models import CarMake, CarModel

# -----------------------------
# Inline class to show CarModels under CarMake
# -----------------------------
class CarModelInline(admin.TabularInline):
    model = CarModel           # Model to show inline
    extra = 1                  # Number of extra blank CarModels to show
    fields = ('name', 'type', 'year', 'dealership_id', 'color', 'price')
    show_change_link = True     # Allow link to edit the model fully

# -----------------------------
# Admin class for CarMake
# -----------------------------
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded_year')  # Columns to show in admin list
    search_fields = ('name', 'country')                # Allow searching by name or country
    inlines = [CarModelInline]                          # Include CarModels inline

# -----------------------------
# Admin class for CarModel (optional, full separate view)
# -----------------------------
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year', 'dealership_id', 'price')
    list_filter = ('type', 'year', 'car_make')        # Filter options in the sidebar
    search_fields = ('name', 'car_make__name')       # Allow search by model or make

# -----------------------------
# Register the models with admin
# -----------------------------
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
