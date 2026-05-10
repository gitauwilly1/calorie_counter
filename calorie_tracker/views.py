from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import FoodItem
from .forms import FoodItemForm


def index(request):
    # Get today's date
    today = timezone.now().date()
    
    # Get all food items for today
    food_items = FoodItem.objects.filter(date_added__date=today)
    
    # Calculate total calories for today
    total_calories = FoodItem.get_total_calories_today()
    
    # Create form for adding new food items
    form = FoodItemForm()
    
    context = {
        'food_items': food_items,
        'total_calories': total_calories,
        'form': form,
    }
    
    return render(request, 'calorie_tracker/index.html', context)


def add_food_item(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.date_added = timezone.now()
            food_item.save()
            messages.success(request, f'Added {food_item.name} ({food_item.calories} calories) successfully!')
            return redirect('index')
        else:
            # If form is invalid, re-render index with errors
            today = timezone.now().date()
            food_items = FoodItem.objects.filter(date_added__date=today)
            total_calories = FoodItem.get_total_calories_today()
            
            context = {
                'food_items': food_items,
                'total_calories': total_calories,
                'form': form,
            }
            return render(request, 'calorie_tracker/index.html', context)
    
    return redirect('index')


def remove_food_item(request, item_id):
    food_item = get_object_or_404(FoodItem, id=item_id)
    name = food_item.name
    food_item.delete()
    messages.success(request, f'Removed {name} successfully!')
    return redirect('index')


def reset_calories(request):
    if request.method == 'POST':
        count = FoodItem.reset_daily_calories()
        if count > 0:
            messages.success(request, f'Reset complete! Removed {count} food items from today.')
        else:
            messages.info(request, 'No food items to reset for today.')
    
    return redirect('index')