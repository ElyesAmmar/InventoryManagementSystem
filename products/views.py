from django.db import IntegrityError, DataError
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from products.models import Products
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_products(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            products = Products(
            name = data.get('name'),
            price = data.get('price'),
            stock= data.get('stock'),
            image = data.get('image'),
            barcode = data.get('barcode')
            )
            products.save()
            return HttpResponse('adding products successfully')
        except (IntegrityError, ValueError, json.JSONDecodeError, DataError) as e:
            return HttpResponse('errors {}'.format(e), status=400)

def get_products(request):
    if request.method == 'GET':
        try:
            data_objects = Products.objects.all()
            array = []
            for obj in data_objects:
                array.append({
                    'name': obj.name,
                    'price': obj.price,
                    'stock': obj.stock,
                    'image': obj.image,
                    'barcode': obj.barcode
                })
            return JsonResponse({'data': array})
            # return HttpResponse(data_objects)
        except:
            return HttpResponse('errors')
