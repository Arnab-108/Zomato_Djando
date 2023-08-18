from django.shortcuts import render,redirect
from django.http import HttpResponse
# views.py
from .models import MenuItem, Order

# Define the display_menu view
chat_history=[]


def display_menu(request):
    menu_items = MenuItem.objects.all()
    orders = Order.objects.all()
    context = {'menu_items': menu_items, 'orders': orders}
    return render(request, 'dish.html', context)

def add_dish(request):
    if request.method == 'POST':
        dish_name = request.POST.get('dish_name')
        price = float(request.POST.get('price'))
        availability = bool(request.POST.get('availability'))
        new_dish = MenuItem(dish_name=dish_name, price=price, availability=availability)
        new_dish.save()
        print(price)
        return redirect('display_menu')
    return render(request , 'add_dish.html')

def remove_dish(request, dish_id):
    dish = MenuItem.objects.get(id=dish_id)
    dish.delete() 
    return redirect('display_menu')

def update(request, dish_id):
    if request.method == 'POST':
        dish = MenuItem.objects.get(id=dish_id)
        dish.dish_name = request.POST.get('dish_name')
        dish.price = float(request.POST.get('price'))
        dish.availability = bool(request.POST.get('availability'))
        dish.save()
        return redirect('display_menu')

    dish = MenuItem.objects.get(id=dish_id)
    return render(request, 'update.html', {'dish': dish})

def take_order(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        selected_dish_ids = request.POST.getlist('selected_dishes')
        
        if customer_name and selected_dish_ids:
            order = Order(customer_name=customer_name, dish_ids=selected_dish_ids, status='received' , rating=0.0 , review = "None")
            order.save()

        return redirect('display_menu')

    menu_items = MenuItem.objects.all()
    return render(request, 'orders.html', {'menu_items': menu_items})

def update_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse("Order not found", status=404)

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        new_rating = int(request.POST.get('new_rating'))
        new_review = request.POST.get('new_review')

        order.status = new_status
        order.rating = new_rating
        order.review = new_review
        order.save()

        return redirect('display_menu')

    return render(request, 'update_order.html', {'order': order})


def chatbot(request):

    if request.method == 'POST':
        user_message = request.POST.get('user_message')
        chatbot_response = generate_chatbot_response(user_message)
        chat_history.append({'user': user_message, 'chatbot': chatbot_response})
    else:
        user_message = None
        chatbot_response = None

    return render(request, 'chatbot.html', {
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
    elif user_message == "hi":
        return 'Hello! How can I assist you today? </br>'
    elif user_message == 'bye':
        return 'Goodbye! Have a great day! </br>'   
    else:
        return "I'm sorry, I didn't understand your message." 
