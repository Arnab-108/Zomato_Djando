from django import template
from zomato.models import MenuItem  # Replace 'myapp' with your actual app name

register = template.Library()

@register.filter
def get_dish_name(dish_id):
    try:
        dish = MenuItem.objects.get(id=dish_id)
        return dish.dish_name
    except MenuItem.DoesNotExist:
        return "Unknown Dish"
