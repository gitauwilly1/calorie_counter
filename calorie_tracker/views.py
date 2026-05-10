from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import FoodItem
from .forms import FoodItemForm


def index(request):
    # Get the date from query params, default to today
    date_str = request.GET.get('date')
    
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = timezone.now().date()
            messages.error(request, 'Invalid date format. Showing today\'s data.')
    else:
        selected_date = timezone.now().date()
    
    # Get food items for the selected date
    food_items = FoodItem.objects.filter(date_added__date=selected_date)
    
    # Calculate total calories for the selected date
    total_calories = sum(item.calories for item in food_items)
    
    # Get all unique dates that have food items (for the date picker)
    dates_with_items = FoodItem.objects.dates('date_added', 'day', order='DESC')
    
    # Calculate weekly summary
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())  # Monday
    weekly_items = FoodItem.objects.filter(
        date_added__date__gte=week_start,
        date_added__date__lte=today
    )
    
    # Weekly totals per day
    weekly_summary = {}
    for item in weekly_items:
        day = item.date_added.date()
        if day not in weekly_summary:
            weekly_summary[day] = 0
        weekly_summary[day] += item.calories
    
    # Create form for adding new food items
    form = FoodItemForm()
    
    context = {
        'food_items': food_items,
        'total_calories': total_calories,
        'form': form,
        'selected_date': selected_date,
        'dates_with_items': dates_with_items,
        'weekly_summary': weekly_summary,
        'today': today,
    }
    
    return render(request, 'index.html', context)


def add_food_item(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food_item = form.save(commit=False)
            
            # Check if a specific date was provided
            date_str = request.POST.get('date_added')
            if date_str:
                try:
                    # Parse the date and set it (keeping the current time)
                    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    current_time = timezone.now().time()
                    food_item.date_added = timezone.make_aware(
                        datetime.combine(selected_date, current_time)
                    )
                except ValueError:
                    food_item.date_added = timezone.now()
            else:
                food_item.date_added = timezone.now()
            
            food_item.save()
            messages.success(
                request, 
                f'Added {food_item.name} ({food_item.calories} calories) successfully!'
            )
            
            # Redirect back to the same date view
            redirect_date = food_item.date_added.strftime('%Y-%m-%d')
            return redirect(f'/?date={redirect_date}')
        else:
            # If form is invalid, re-render with errors
            selected_date = request.GET.get('date', timezone.now().date())
            if isinstance(selected_date, str):
                try:
                    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
                except ValueError:
                    selected_date = timezone.now().date()
            
            food_items = FoodItem.objects.filter(date_added__date=selected_date)
            total_calories = sum(item.calories for item in food_items)
            dates_with_items = FoodItem.objects.dates('date_added', 'day', order='DESC')
            
            context = {
                'food_items': food_items,
                'total_calories': total_calories,
                'form': form,
                'selected_date': selected_date,
                'dates_with_items': dates_with_items,
            }
            return render(request, 'index.html', context)
    
    return redirect('index')


def remove_food_item(request, item_id):
    food_item = get_object_or_404(FoodItem, id=item_id)
    item_date = food_item.date_added.strftime('%Y-%m-%d')
    name = food_item.name
    food_item.delete()
    messages.success(request, f'Removed {name} successfully!')
    return redirect(f'/?date={item_date}')


def reset_calories(request):
    if request.method == 'POST':
        date_str = request.POST.get('date')
        if date_str:
            try:
                selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                selected_date = timezone.now().date()
        else:
            selected_date = timezone.now().date()
        
        count = FoodItem.objects.filter(date_added__date=selected_date).count()
        FoodItem.objects.filter(date_added__date=selected_date).delete()
        
        if count > 0:
            messages.success(
                request, 
                f'Reset complete! Removed {count} food items from {selected_date}.'
            )
        else:
            messages.info(request, f'No food items to reset for {selected_date}.')
    
    return redirect('index')


def weekly_summary_api(request):
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    
    weekly_data = []
    for i in range(7):
        day = week_start + timedelta(days=i)
        day_items = FoodItem.objects.filter(date_added__date=day)
        total = sum(item.calories for item in day_items)
        count = day_items.count()
        
        weekly_data.append({
            'date': day.strftime('%Y-%m-%d'),
            'day_name': day.strftime('%A'),
            'total_calories': total,
            'items_count': count,
        })
    
    return JsonResponse({'weekly_data': weekly_data, 'goal': 2000})