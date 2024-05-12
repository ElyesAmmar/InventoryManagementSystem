from django.db import IntegrityError, DataError
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Orders, OrdersItems
from products.models import Products
from customers.models import Customers
import json
from reportlab.pdfgen import canvas
from django.views.decorators.csrf import csrf_exempt


def get_orders(request, user_id):
    if request.method == 'GET':
        try:
            orders = []
            # check if the request is filtring by date
            if request.body:
                data = json.loads(request.body)
                if len(data) > 0:
                    orders = Orders.objects.filter(
                        user_id= user_id,
                        created_at__gte= data['date'][0],
                        created_at__lte= data['date'][1]
                        )
            # else if not filtring by date get all the orders
            else:
                orders = Orders.objects.filter(user_id= user_id)

            array = []
            for ord in orders:
                array.append({
                    'user_id': ord.user_id,
                    'order_num': ord.order_num,
                    'created_at': ord.created_at,
                    'customer_id': ord.customer_id,
                    'total_amount': ord.total_amount,
                    'shipping_address': ord.shipping_address
                })
            return JsonResponse({'data': array})
        except(IntegrityError, ValueError, json.JSONDecodeError, DataError, TypeError) as e:
            return HttpResponse('errors {}'.format(e), status=400)

@csrf_exempt
def create_order(request, user_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # generating order num
            order_num = 10001
            orders = Orders.objects.filter(user_id= user_id)
            last_order = orders.order_by('-order_num').first()
            if last_order:
                order_num = last_order.order_num + 1
            
            # calculating the total amount
            total_amount = 0
            for prod in data['products']:
                total_amount += prod['quantity'] * prod['unit_price']

            order = Orders(
                user_id = user_id,
                order_num = order_num,
                customer_id = data['customer_id'],
                total_amount = total_amount,
                shipping_address = data['shipping_address']
            )
            order.save()

            # create each product item
            for prod in data['products']:
                order_items = OrdersItems(
                    order_id = order.id,
                    product_id = prod['product_id'],
                    quantity = prod['quantity'],
                    unit_price = prod['unit_price'],
                    total_price = prod['quantity'] * prod['unit_price']
                )
                order_items.save()

            return HttpResponse('creating order successfully')
        except(IntegrityError, ValueError, json.JSONDecodeError, DataError, TypeError) as e:
            return HttpResponse('errors {}'.format(e), status=400)

@csrf_exempt
def update_order(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order = Orders.objects.get(pk= id)
            
            # update products if exist changes on it, in the table OrdersItems
            if 'products' in list(data.keys()):
                for prod in data['products']:
                    order_item = OrdersItems.objects.get(pk = prod['orders_items_id'])
                    for key, value in prod.items():
                        setattr(order_item, key, value)
                    order_item.total_price = prod['quantity'] * prod['unit_price']
                    order_item.save()
                
                # update total_amount in order if having changes on products
                total_amount = 0
                for prod in data['products']:
                    total_amount += prod['quantity'] * prod['unit_price']
                order.total_amount = total_amount
                order.save()

            # update the rest of order data if exist changes
            if 'order' in list(data.keys()):
                for key, value in data['order'].items():
                    setattr(order, key, value)
                order.save()

            return HttpResponse('updating order successfully')
        except(IntegrityError, ValueError, json.JSONDecodeError, DataError, TypeError) as e:
            return HttpResponse('errors {}'.format(e), status=400)

# retrieve order from db
def get_order_function(id):
    order = Orders.objects.get(pk = id)
    customer = Customers.objects.get(pk = order.customer_id)
    order_items = OrdersItems.objects.filter(order_id = id)
    products = []
    for item in order_items:
        product = Products.objects.get(pk = item.product_id)
        products.append({
            'name': product.name,
            'unit_price': item.unit_price,
            'quantity': item.quantity,
            'total_price': item.total_price
        })
    order_data = {
        'order_num': order.order_num,
        'order_date': order.created_at,
        'customer': {
            'name': customer.name,
            'address': customer.adresse,
            'phone': customer.phone,
            'company': customer.company,
            'email': customer.email
        },
        'shipping_address': order.shipping_address,
        'products': products,
        'total_amount': order.total_amount
    }
    return order_data

# send json order to client side 
def get_order_details(request, id):
    if request.method == 'GET':
        try:
            order_data = get_order_function(id)
            return JsonResponse(order_data)
        except(IntegrityError, ValueError, json.JSONDecodeError, DataError, TypeError) as e:
            return HttpResponse('errors {}'.format(e), status=400)

def generate_invoice(request, id):
    from reportlab.lib.colors import pink, black, red, blue, green
    try:
        from io import BytesIO

        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # create invoice pdf 
        order = get_order_function(id)

        p.drawString(50, 800, "Title")

        
        # company details
        p.drawString(400, 800, "Elyes Ammar")
        p.setFillColor(red)
        p.setFont("Times-Roman", 20)
        p.drawString(400, 780, "8000 Nabeul")
        p.drawString(400, 760, "50253720")

        #customer details
        p.drawString(50, 700, "Invoice")
        p.drawString(50, 680, "Billed to:")
        p.drawString(50, 660, f"{order['customer']['name']}")
        p.drawString(50, 640, f"{order['customer']['address']}")
        p.drawString(50, 620, f"{order['customer']['company']}")
        p.drawString(50, 600, f"{order['customer']['phone']}")
        
        p.drawString(350, 680, f"Invoice No: {order['order_num']}")
        p.drawString(350, 660, f"Date: {order['order_date']}")
        
        #products details
        p.drawString(70, 550, "Items")
        p.drawString(250, 550, "Quantity")
        p.drawString(350, 550, "Unit price")
        p.drawString(450, 550, "Total")

        y = 520
        for prod in order['products']:
            p.drawString(60, y, f"{prod['name']}")
            p.drawString(250, y, f"{prod['quantity']}")
            p.drawString(350, y, f"{prod['unit_price']}")
            p.drawString(450, y, f"{prod['total_price']}")
            y-= 30
        p.showPage()
        p.save()

        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename=f'invoice {order['order_num']}.pdf')

    except(IntegrityError, ValueError, json.JSONDecodeError, DataError, TypeError) as e:
            return HttpResponse('errors {}'.format(e), status=400)


