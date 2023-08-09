from django.shortcuts import render,redirect

# Create your views here.
menu = {
    1: {'name': 'Pasta', 'price': 8.99, 'available': True},
    2: {'name': 'Pizza', 'price': 10.99, 'available': True},
    3: {'name': 'Burger', 'price': 6.99, 'available': True},
    4:{'name':'Biriyani','price':11.99, 'available':True},
    5:{'name':'Chicken  Chap','price':13.99, 'available':True},
}

orders={}
# Define the get_menu() function
def get_menu():
    return menu

# Define the display_menu view
def display_menu(request):
    menu = get_menu()
    context = {'menu': menu, 'orders': orders}
    return render(request, 'dish.html', context)

def add_dish(request):
    if request.method == 'POST':
        menu = get_menu()
        dish_id = len(menu)+1
        dish_name = request.POST['dish_name']
        dish_price = float(request.POST['dish_price'])
        available = request.POST.get('available', False) == 'on'
        menu[dish_id] = {'name': dish_name, 'price': dish_price, 'available': available}
        return redirect('display_menu')
    return render(request , 'add_dish.html')

def remove_dish(request, dish_id):
    menu = get_menu()  
    if dish_id in menu:
        del menu[dish_id]  
    return redirect('display_menu')

def update_availability(request, dish_id):
    menu = get_menu()
    if dish_id in menu:
        menu[dish_id]['available'] = not menu[dish_id]['available']
    return redirect('display_menu')

def take_order(request):
    menu = get_menu()  # Get the current menu
    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        dish_ids = request.POST.getlist('selected_dishes')
        new_order = {'customer_name': customer_name, 'dishes': []}
        for dish_id in dish_ids:
            if int(dish_id) in menu:
                new_order['dishes'].append(menu[int(dish_id)]['name'])
        # Assign a new order ID
        order_id = len(orders) + 1
        orders[order_id] = {'order': new_order, 'status': 'received'}
        print(orders)
        print(dish_ids)
        print(new_order)
        return redirect('display_menu')
    return render(request, 'orders.html', {'menu': menu})

def update_status(request, order_id):
    if order_id in orders:
        orders[order_id]['status'] = 'done'
    return redirect('display_menu')