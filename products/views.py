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

def get_products(request, user_id):
    if request.method == 'GET':
        try:
            data_objects = Products.objects.filter(user_id= user_id)
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
            # return HttpResponse(data_objects.values())
        except (IntegrityError, ValueError, json.JSONDecodeError, DataError, TypeError) as e:
            return HttpResponse('errors {}'.format(e), status=400)

@csrf_exempt   
def update_product(request, id):
    if request.method == 'PUT':
        try:
            req = json.loads(request.body)
            # prod = Products.objects.filter(id=_id)
            product = Products.objects.get(pk=id)

            # update product depending on the request key & value
            for key, value in req.items():
                setattr(product, key, value)
            product.save()

            return HttpResponse('updating product successfully')
        
        except(IntegrityError, ValueError, json.JSONDecodeError, DataError, TypeError) as e:
            return HttpResponse('errors {}'.format(e), status=400)
        
    if request.method == 'DELETE':
        try:
            product = Products.objects.get(pk=id)
            product.delete()
            return HttpResponse('product deleted successfully')
        
        except(IntegrityError, ValueError, json.JSONDecodeError, DataError, TypeError) as e:
            return HttpResponse('errors {}'.format(e), status=400)

def filter_products(request):
    if request.method == 'GET':
        try:
            req = json.loads(request.body)
            product = {}
            #filter by barcode 
            if list(req.keys())[0] == 'barcode':
                product = Products.objects.filter(barcode= req['barcode'])
            
            # filter by name
            if list(req.keys())[0] == 'name':
                product = Products.objects.filter(user_id= req['user_id'], name__contains= req['name'])
                
            array = []
            for obj in product:
                array.append({
                    'name': obj.name,
                    'price': obj.price,
                    'stock': obj.stock,
                    'image': obj.image,
                    'barcode': obj.barcode
                })
            return JsonResponse({'data': array})
        
        except(IntegrityError, ValueError, json.JSONDecodeError, DataError, TypeError) as e:
            return HttpResponse('errors {}'.format(e), status=400)

