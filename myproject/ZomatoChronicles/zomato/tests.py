from django.test import TestCase
from django.urls import reverse
from .models import MenuItem, Order
from .views import display_menu
from mongoengine import connect

class ZomatoTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Connect to your MongoDB
        connect('test_zomato_db', host='mongodb+srv://arnabadhikary007:arnabadhikary@cluster0.xrv0a3m.mongodb.net/test_zomato_db?retryWrites=true&w=majority')
    
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Clean up the database after all tests
        MenuItem.objects.all().delete()
        Order.objects.all().delete()

class DisplayMenuViewTest(ZomatoTestCase):
    def test_display_menu(self):
        # Create some test data (menu items and orders) using your models
        MenuItem(dish_name='Pizza', price=10, availability=True).save()
        MenuItem(dish_name='Burger', price=5, availability=True).save()
        Order(customer_name='John', dish_ids=['64d5007293873bc43bed668d'], status='received').save()
        Order(customer_name='Alice', dish_ids=['64d5cfe5e57c5c1b4f3b7a40'], status='received').save()
        
        # Create a request using the reverse function to get the URL
        url = reverse('display_menu')
        
        # Use the client's get method to simulate a GET request
        response = self.client.get(url)
        
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

class AddDishViewTest(ZomatoTestCase):
    def test_add_dish(self):
        # Send a POST request to the add_dish view
        response = self.client.post(reverse('add_dish'), {
            'dish_name': 'New Dish',
            'price': '10.99',  # Float value as a string
            'availability': 'True'  # Boolean value as a string
        })

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that a new menu item is created
        self.assertEqual(MenuItem.objects.count(), 1)

        # Retrieve the created menu item and verify its attributes
        new_dish = MenuItem.objects.first()
        self.assertEqual(new_dish.dish_name, 'New Dish')
        self.assertAlmostEqual(new_dish.price, 10.99)  # Use assertAlmostEqual for floating-point comparisons
        self.assertTrue(new_dish.availability)

        # Check that the user is redirected to the display_menu page
        self.assertRedirects(response, reverse('display_menu'))

class RemoveDishViewTest(ZomatoTestCase):
    def test_remove_dish(self):
        # Create a menu item for testing
        dish = MenuItem(dish_name='Test Dish', price=10.99, availability=True)
        dish.save()
        
        # Get the URL for the remove_dish view, passing the dish_id as an argument
        url = reverse('remove_dish', args=[str(dish.id)])
        
        # Use the client's post method to simulate a POST request
        response = self.client.post(url)
        
        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the menu item has been deleted from the database
        self.assertEqual(MenuItem.objects.count(), 0)

        # Check that the user is redirected to the display_menu page
        self.assertRedirects(response, reverse('display_menu'))


class UpdateDishViewTest(ZomatoTestCase):
    def test_update_dish(self):
    # Create a test dish
        dish = MenuItem(dish_name='Test Dish', price=10.99, availability=True)
        dish.save()

        # Prepare data for the POST request
        updated_dish_name = 'Updated Dish'
        updated_price = '15.99'
        updated_availability = 'false'  # Use lowercase for boolean values

        # Send a POST request to the update view with updated data
        response = self.client.post(reverse('update', args=[dish.id]), {
            'dish_name': updated_dish_name,
            'price': updated_price,
            'availability': updated_availability,
        })

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Retrieve the updated dish from the database
        updated_dish = MenuItem.objects.get(id=dish.id)

        # Check that the dish attributes have been updated
        self.assertEqual(updated_dish.dish_name, updated_dish_name)
        self.assertAlmostEqual(updated_dish.price, float(updated_price))
        self.assertTrue(updated_dish.availability)  # Ensure availability is False
        # Check that the user is redirected to the display_menu page
        self.assertRedirects(response, reverse('display_menu'))


    def test_update_dish_get(self):
        # Create a test dish
        dish = MenuItem(dish_name='Test Dish', price=10.99, availability=True)
        dish.save()

        # Send a GET request to the update view
        response = self.client.get(reverse('update', args=[dish.id]))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used for rendering
        self.assertTemplateUsed(response, 'update.html')

        # Check that the response context contains the dish data
        self.assertEqual(response.context['dish'], dish)


class TakeOrderViewTest(ZomatoTestCase):
    def test_take_order(self):
        # Create a test menu item
        menu_item = MenuItem(dish_name='Pizza', price=10, availability=True)
        menu_item.save()

        # Prepare data for the POST request
        customer_name = 'John'
        selected_dishes = [str(menu_item.id)]

        # Send a POST request to the take_order view with order data
        response = self.client.post(reverse('take_order'), {
            'customer_name': customer_name,
            'selected_dishes': selected_dishes,
        })

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Retrieve the created order from the database
        order = Order.objects.first()

        # Check that the order attributes are correctly set
        self.assertEqual(order.customer_name, customer_name)
        self.assertEqual(order.dish_ids, selected_dishes)
        self.assertEqual(order.status, 'received')
        self.assertEqual(order.rating, 0.0)
        self.assertEqual(order.review, 'None')

        # Check that the user is redirected to the display_menu page
        self.assertRedirects(response, reverse('display_menu'))

class UpdateStatusViewTest(ZomatoTestCase):
    def test_update_status_valid(self):
        # Create a test order
        order = Order(customer_name='John Doe', dish_ids=['64d5007293873bc43bed668d', '64d5cfe5e57c5c1b4f3b7a40'], status='received', rating=0, review='')
        order.save()

        # Prepare the POST request data
        new_status = 'completed'
        new_rating = 4
        new_review = 'Great service!'

        # Send a POST request to the update_status view with the prepared data
        response = self.client.post(reverse('update_status', args=[order.id]), {
            'new_status': new_status,
            'new_rating': new_rating,
            'new_review': new_review,
        })

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Retrieve the updated order from the database
        updated_order = Order.objects.get(id=order.id)

        # Check that the order attributes have been updated
        self.assertEqual(updated_order.status, new_status)
        self.assertEqual(updated_order.rating, new_rating)
        self.assertEqual(updated_order.review, new_review)

        # Check that the user is redirected to the display_menu page
        self.assertRedirects(response, reverse('display_menu'))