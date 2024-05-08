from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from customers.models import Customers
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def add_customers(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # data = {
            #     "name": "Elyes Ammar",
            #     "adresse": "Nabeul",
            #     "phone": 9385474,
            #     "company": "Ayshek",
            #     "email": "elyes@gmail.com",
            #     "user_id": 7
            # }
            customers = Customers(
                name = data['name'],
                adresse = data['adresse'],
                phone = data['phone'],
                company = data['company'],
                email = data['email'],
                user_id =data['user_id']
            )
            customers.save()
            return HttpResponse('addibg customers successfully')
        except:
            return HttpResponse('errors')