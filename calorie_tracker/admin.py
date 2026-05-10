from django.contrib import admin
from django.utils.html import format_html
from .models import FoodItem


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    # Display columns in the list view
    list_display = ['name', 'calories', 'calorie_level', 'added_today', 'date_added']
    
    # Filter options
    list_filter = ['date_added']
    
    # Search fields
    search_fields = ['name']
    
    # Default ordering
    ordering = ['-date_added']
    
    # Fields per page
    list_per_page = 25
    
    # Read-only fields (can't be edited in admin)
    readonly_fields = ['date_added']
    
    # Fields grouping in edit form
    fieldsets = (
        ('Food Information', {
            'fields': ('name', 'calories')
        }),
        ('Metadata', {
            'fields': ('date_added',),
            'classes': ('collapse',)
        }),
    )
    
    @admin.display(description='Calorie Level', ordering='calories')
    def calorie_level(self, obj):
        if obj.calories > 500:
            color = 'red'
            label = 'High'
        elif obj.calories > 200:
            color = 'orange'
            label = 'Medium'
        else:
            color = 'green'
            label = 'Low'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">● {} ({} cal)</span>',
            color, label, obj.calories
        )
    
    @admin.display(description='Added Today', boolean=True)
    def added_today(self, obj):
        from django.utils import timezone
        today = timezone.now().date()
        is_today = obj.date_added.date() == today
        
        if is_today:
            return True
        return False
    
    # Custom actions
    actions = ['mark_as_high_calorie', 'delete_today_items']
    
    @admin.action(description="Mark selected as High Calorie (999 cal)")
    def mark_as_high_calorie(self, request, queryset):
        updated = queryset.update(calories=999)
        self.message_user(
            request,
            f'{updated} food items were marked as high calorie (999 cal).'
        )
    
    @admin.action(description="Delete today's items from selected")
    def delete_today_items(self, request, queryset):
        from django.utils import timezone
        today = timezone.now().date()
        today_items = queryset.filter(date_added__date=today)
        count = today_items.count()
        today_items.delete()
        self.message_user(
            request,
            f'{count} food items from today were deleted.'
        )