from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from products.models import Products

def add_products(request):
    try:
        products = Products(
        name = 'carte graphique',
        price = 500,
        stock= 9,
        image = 'https://www.sbsinformatique.com/8163/tunisie/large/carte-graphique-asus-rog-strix-geforce-rtx-3080-ti-oc-12g-gaming-tunisie.jpg',
        barcode = 748374856
        )
        products.save()
        # return render(request, 'response.html', {'product': product})
        return HttpResponse('adding products successfully')
    except IntegrityError as e:
        return HttpResponse('errors {}'.format(e))

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
