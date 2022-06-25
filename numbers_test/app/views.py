from django.shortcuts import render
from .models import Order
from django.http import JsonResponse

# Create your views here.

def orders(request):
    orders = Order.objects.all()
    result = []
    for order in orders:
        total_cost = [str(order.total_cost_in_rubles), str(order.total_cost_in_rubles_after_comma)]
        print(total_cost)
        order_total_cost_in_rubles = '.'.join(total_cost)
        print(order_total_cost_in_rubles)
        result.append({
            'index_in_table': order.index_in_table,
            'order_id': order.order_id,
            'incoming_date': order.incoming_date,
            'total_cost_in_dollars': order.total_cost_in_dollars,
            'total_cost_in_rubles': order_total_cost_in_rubles,
        })
    return JsonResponse(result, safe=False)
    