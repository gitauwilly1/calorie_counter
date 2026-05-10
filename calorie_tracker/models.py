from django.db import models
from django.utils import timezone


class FoodItem(models.Model):
    name = models.CharField(max_length=200, help_text="Enter the name of the food item")
    calories = models.PositiveIntegerField(help_text="Enter the number of calories")
    date_added = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-date_added']  # Order by most recent first
        verbose_name = "Food Item"
        verbose_name_plural = "Food Items"
    
    def __str__(self):
        return f"{self.name} - {self.calories} calories"
    
    @classmethod
    def get_total_calories_today(cls):
        today = timezone.now().date()
        today_items = cls.objects.filter(date_added__date=today)
        return sum(item.calories for item in today_items)
    
    @classmethod
    def reset_daily_calories(cls):
        today = timezone.now().date()
        today_items = cls.objects.filter(date_added__date=today)
        count = today_items.count()
        today_items.delete()
        return count