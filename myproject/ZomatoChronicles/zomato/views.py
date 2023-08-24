from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
# views.py
from .models import MenuItem, Order
from django.views.decorators.csrf import csrf_exempt
import json

# Define the display_menu view

chat_history=[]


def display_menu(request):
    menu_items = MenuItem.objects.all()
    menu_data = []
    for item in menu_items:
        menu_data.append({
            '_id': str(item.id),
            'dish_name': item.dish_name,
            'price': item.price,
            'availability': item.availability
        })
    return JsonResponse({'menu_items': menu_data})

def display_orders(request):
    orders = Order.objects.all()
    order_data = []

    for order in orders:
        order_data.append({
            '_id': str(order.id),
            'customer_name': order.customer_name,
            'dish_ids': order.dish_ids, 
            'status': order.status,
            'rating': order.rating,
            'review': order.review
        })

    return JsonResponse({'orders': order_data})

@csrf_exempt
def add_dish(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            dish_name = data.get('dish_name')
            price = data.get('price')
            availability = data.get('availability')

            if price is None:
                return JsonResponse({'error': 'Price is missing'}, status=400)

            try:
                price = float(price)
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Invalid price format'}, status=400)

            new_dish = MenuItem(dish_name=dish_name, price=price, availability=availability)
            new_dish.save()
            return JsonResponse({'message': 'Dish added successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def remove_dish(request, dish_id):
    try:
        dish = MenuItem.objects.get(id=dish_id)
        dish.delete()
        return JsonResponse({'message': 'Dish removed successfully'})
    except MenuItem.DoesNotExist:
        return JsonResponse({'error': 'Dish not found'}, status=404)
    
@csrf_exempt
def update(request, dish_id):
    try:
        dish = MenuItem.objects.get(id=dish_id)
    except MenuItem.DoesNotExist:
        return JsonResponse({'error': 'Dish not found'}, status=404)

    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)  # Parse the JSON data from the request body
            dish.dish_name = data.get('dish_name', dish.dish_name)  # Use the existing dish name if not provided
            dish.price = float(data.get('price', dish.price))
            dish.availability = bool(data.get('availability', dish.availability))
            dish.save()
            return JsonResponse({'message': 'Dish updated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def take_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse the JSON data from the request body
            customer_name = data.get('customer_name')
            selected_dish_ids = data.get('dish_ids', [])
            
            if customer_name and selected_dish_ids:
                order = Order(customer_name=customer_name, dish_ids=selected_dish_ids, status='received', rating=0.0, review="None")
                order.save()
                return JsonResponse({'message': 'Order placed successfully'})
            else:
                return JsonResponse({'error': 'Customer name and dish IDs are required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def update_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    if request.method == 'PATCH':
        try:
            data = json.loads(request.body.decode('utf-8'))  # Decode the bytes and parse JSON
            new_status = data.get('new_status')
            new_rating = data.get('new_rating')
            new_review = data.get('new_review')

            if new_rating is not None:
                try:
                    new_rating = int(new_rating)
                except ValueError:
                    return JsonResponse({'error': 'Invalid rating value'}, status=400)

            order.status = new_status
            order.rating = new_rating
            order.review = new_review
            order.save()

            return JsonResponse({'message': 'Status updated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
@csrf_exempt
def chatbot(request):
    global chat_history  # Access the global chat_history variable

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))  # Decode the bytes and parse JSON
        user_message = data.get('user_message')
        chatbot_response = generate_chatbot_response(user_message)
        chat_history.append({'user': user_message, 'chatbot': chatbot_response})
    else:
        user_message = None
        chatbot_response = None

    return JsonResponse({
        'user_message': user_message,
        'chatbot_response': chatbot_response,
        'chat_history': chat_history
    })



def generate_chatbot_response(user_message):
    user_message = user_message.lower()

    if user_message == 'menu':
        menu_items = MenuItem.objects.all()
        menu_response = "<strong>Here's the list of available dishes:</strong><ul>"
        for item in menu_items:
            menu_response += f"<li>{item.dish_name}</li>"
        menu_response += "</ul>"
        return menu_response
    elif user_message == 'order':
        order_response = '<strong>Sure, let me help you place an order.:</strong> <ol> <li> In the homepage you should see a Take New Order button.</li> <li> Click the button.</li> <li> Then you will be redirected to the Take New Orders Page.</li> <li> After being redirected just follow the form and press the submit button. A new order will be created.</li> </ol>'
        return order_response
    elif user_message == "hi" :
        return 'Hello! How can I assist you today? </br>'
    elif user_message == 'bye':
        return 'Goodbye! Have a great day! </br>'   
    else:
        return "I'm sorry, I didn't understand your message." 
