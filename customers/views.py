from django.shortcuts import render
from django.db import IntegrityError, DataError
from django.http import HttpResponse, JsonResponse
from customers.models import Customers
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def add_customers(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customers = Customers(
                name = data['name'],
                adresse = data['adresse'],
                phone = data['phone'],
                company = data['company'],
                email = data['email'],
                user_id =data['user_id']
            )
            customers.save()
            # return HttpResponse('adding customers successfully')
            return JsonResponse({
                "id": customers.id,
                "name": customers.name,
                "adresse": customers.adresse,
                "phone": customers.phone,
                "company": customers.company,
                "email": customers.email,
                "user_id": customers.user_id
                })
        except(IntegrityError, ValueError, json.JSONDecodeError, DataError) as e:
            return HttpResponse('errors {}'.format(e), status=400)
        
def get_customers(request, user_id):
    if request.method == 'GET':
        try:
            data_objects = Customers.objects.filter(user_id= user_id)
            array = []
            for obj in data_objects:
                array.append({
                    'name': obj.name,
                    'adresse': obj.adresse,
                    'email': obj.email,
                    'company': obj.company,
                    'phone': obj.phone
                })
            # return JsonResponse({'msg': 'getting customers successfully', 'data': array})
            return HttpResponse(data_objects.values())
        except (IntegrityError, ValueError, json.JSONDecodeError, DataError, TypeError) as e:
            return HttpResponse('errors {}'.format(e), status=400)
        
@csrf_exempt   
def update_customers(request, id):
    if request.method == 'PUT':
        try:
            req = json.loads(request.body)
            # prod = Customers.objects.filter(id=_id)
            customer = Customers.objects.get(pk=id)

            # update customer depending on the request key & value
            for key, value in req.items():
                setattr(customer, key, value)
            customer.save()

            return HttpResponse('updating customer successfully')
        
        except(IntegrityError, ValueError, json.JSONDecodeError, DataError, TypeError) as e:
            return HttpResponse('errors {}'.format(e), status=400)
        
    if request.method == 'DELETE':
        try:
            customer = Customers.objects.get(pk=id)
            customer.delete()
            return HttpResponse('customer deleted successfully')
        
        except(IntegrityError, ValueError, json.JSONDecodeError, DataError, TypeError) as e:
            return HttpResponse('errors {}'.format(e), status=400)
        
def filter_customers(request):
    if request.method == 'GET':
        try:
            req = json.loads(request.body)
            customer = {}
            #filter by barcode 
            if list(req.keys())[0] == 'email':
                customer = Customers.objects.filter(email= req['email'])
            
            # filter by name
            if list(req.keys())[0] == 'name':
                customer = Customers.objects.filter(user_id= req['user_id'], name__icontains= req['name'])
                
            array = []
            for obj in customer:
                array.append({
                    'name': obj.name,
                    'adresse': obj.adresse,
                    'email': obj.email,
                    'company': obj.company,
                    'phone': obj.phone
                })
            return JsonResponse({'data': array})
        
        except(IntegrityError, ValueError, json.JSONDecodeError, DataError, TypeError) as e:
            return HttpResponse('errors {}'.format(e), status=400)