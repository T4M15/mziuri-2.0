from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse, Http404

PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 1800},
    {"id": 2, "name": "Headphones", "price": 150},
    {"id": 3, "name": "Mouse", "price": 40},
]

def home(request):
    return HttpResponse('<h1>myshop</h1><br><a href="/products/">პროდუქტების სია</a>')

def about(request):
    return HttpResponse('<p>ეს არის ჩვენი ონლაინ მაღაზიის სატესტო პლატფორმა, სადაც ვწავლობთ Django-ს საფუძვლებს.</p>')

def product_list(request):
    items_html = "".join([
        f'<li><a href="/products/{p["id"]}/">{p["name"]}</a>: {p["price"]} ₾</li>'
        for p in PRODUCTS
    ])
    return HttpResponse(f'<ul>{items_html}</ul>')

def product_detail(request, product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        raise Http404("პროდუქტი ვერ მოიძებნა")
    return HttpResponse(f'<h1>{product["name"]}</h1><p>ფასი: {product["price"]} ₾</p>')
