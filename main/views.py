from django.contrib import messages
from django.shortcuts import render,redirect
from .models import MenuSection,Table
from django.views import View
from .models import Reservation
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from bs4 import BeautifulSoup
import requests
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def home(request):
    return render(request,"views/home.html")

def menu(request):
    sections = MenuSection.objects.prefetch_related('items').all()
    return render(request,"views/menu.html",{'sections': sections})


class Reservationcreateview(View):
    def get(self, request):
        tables = Table.objects.filter(is_reserved=False)
        return render(request, 'views/reservation.html', {'tables': tables})

    def post(self, request):
        if not request.user.is_authenticated:
            # If not logged in, show an error message and reload the form
            messages.error(request, 'You must be logged in to make a reservation.')
            tables = Table.objects.filter(is_reserved=False)
            return render(request, 'views/reservation.html', {'tables': tables})
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        number_of_people = request.POST.get('number_of_people')
        table_id = request.POST.get('table')
        date = request.POST.get('date')
        table = Table.objects.get(id=table_id)
        if Reservation.objects.filter(table=table).exists():
            messages.error(request, 'This table is already reserved for the selected time.')
            tables = Table.objects.filter(is_reserved=False)
            return render(request, 'views/reservation.html', {'tables': tables})

        # Create the reservation object
        Reservation.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            email=email,
           
            table=table,
            
        )
        table.is_reserved=True
        table.save()

        # Optionally, you can add some logic to handle success or failure
        # For example, redirect to a success page or show a message
        return redirect('main')
    
from django.shortcuts import render
from .forms import DishForm
from .services import get_recipe_by_dish_name

# recipe/views.py
from django.shortcuts import render

# views.py
import requests
from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.shortcuts import render
from django.conf import settings

import requests
from django.shortcuts import render
from django.conf import settings

def meal_plan(request):
    if request.method == 'POST':
        target_calories = request.POST.get('target_calories')
        diet = request.POST.get('diet')
        
        url = f"https://api.spoonacular.com/mealplanner/generate?apiKey=2aa152d144034dcdac8d3d32a71a912d&timeFrame=day&targetCalories={target_calories}&diet={diet}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            meals = data.get('meals', [])
            nutrients = data.get('nutrients', {})
        else:
            meals = []
            nutrients = {}
        
        context = {
            'meals': meals,
            'nutrients': nutrients,
            'target_calories': target_calories,
            'diet': diet
        }
    else:
        context = {
            'meals': [],
            'nutrients': {},
            'target_calories': '',
            'diet': ''
        }
    return render(request, 'views/reciepe.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import MenuItem, Order, OrderItem

def menu_view(request):
    
    sections = MenuSection.objects.prefetch_related('items').all()
    return render(request, 'views/menu1.html', {'sections': sections})

def add_to_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        menu_item = get_object_or_404(MenuItem, id=item_id)
        
        cart = request.session.get('cart', {})
        if item_id in cart:
            cart[item_id]['quantity'] += quantity
        else:
            cart[item_id] = {'name': menu_item.name, 'price': str(menu_item.price), 'quantity': quantity}
        
        request.session['cart'] = cart
        return JsonResponse({'status': 'success', 'cart': cart})

def view_cart(request):
    cart = request.session.get('cart', {})
    return render(request, 'views/cart.html', {'cart': cart})

def place_order(request):
    if request.method == 'POST':
        table_number = request.POST.get('table_number')
        cart = request.session.get('cart', {})

        order = Order.objects.create(table_number=table_number,user=request.user)
        for item_id, item_data in cart.items():
            menu_item = get_object_or_404(MenuItem, id=item_id)
            OrderItem.objects.create(order=order, menu_item=menu_item, quantity=item_data['quantity'])
        
        request.session['cart'] = {}  # Clear the cart
        return redirect('payment', order_id=order.id)
    
    return redirect('menu')

def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'views/payment.html', {'order': order})
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def scrap(request):
    url = "https://www.health.com/nutrition"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    print(response)
    blog_items = []
    
    # Parse the response content
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the div with the specific id
    dic1 = soup.find('div', id="tax-sc__recirc-list_1-0")
    
    if dic1:
        # Find all anchor tags with the specific class within the div
        as1 = dic1.find_all('a', class_="comp mntl-card-list-items mntl-document-card mntl-card card card--no-image")
        
        for a in as1:
            blog_d = {}
            # Find the img tag with the specific class within the anchor tag
            imgsrc = a.find('img', class_="lazyload card__img universal-image__image")
            if imgsrc:
                blog_d['imgsrc'] = imgsrc['data-src']
                print(imgsrc['data-src'])

            headline = a.find('span', class_="card__title-text")
            if headline:
                print(headline.text)
                blog_d['headline'] = headline.text
            
           
            link = a['href']
            blog_d['link'] = link
            blog_items.append(blog_d)
    else:
        print("No div found with the specified id.")
    
    return render(request, 'views/blog.html', {'blog_items': blog_items})

from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Existing scrap view...

def blog_detail(request, link):
    url = link
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    print(link)
    soup = BeautifulSoup(response.content, "html.parser")

    
    item = soup.find('div', id="mntl-sc-page_1-0")  # Update the class as per actual HTML


    print("hello")
    blog_content={}
    if item:
        paragraph = item.find_all('p',class_="comp mntl-sc-block mntl-sc-block-html") 
        list=[]
        for p in paragraph:
            list.append(p.text)

         # Adjust to get the relevant paragraph
        imgsrc=item.find('img',class_="primary-image__image mntl-primary-image--blurry loaded")
        print(imgsrc)
        if imgsrc:
            blog_content['imgsrc']=imgsrc['data-src']
            print(imgsrc['data-src'])


   
    blog_content['p']=list
    
    
     
    
    return render(request, 'views/blog_content.html', {'blog_content': blog_content})



@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'views/user_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'views/order_detail.html', {'order': order})

