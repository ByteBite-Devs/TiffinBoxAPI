import json
import firebase_admin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import credentials
from pyrebase import pyrebase

config = {
    "apiKey": "AIzaSyDCFuhMxcUAFtR7wiazf8_yV8i4Qcrhzug",
    "authDomain": "tiffinbox-9114a.firebaseapp.com",
    "databaseURL": "https://tiffinbox-9114a-default-rtdb.firebaseio.com",
    "projectId": "tiffinbox-9114a",
    "storageBucket": "tiffinbox-9114a.appspot.com",
    "messagingSenderId": "72750034964",
    "appId": "1:72750034964:web:89f9453d754f3a2a6b3701",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

SERVICE_ACCOUNT_KEY_PATH = "config/serviceAccountKey.json"
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    firebase_admin.initialize_app(cred)



@csrf_exempt
def create_order(request):
    data = json.loads(request.body)
    data["order_status"] = "Placed"
    # create the invouce numver
    orders = db.child("Orders").get().val()
    # find the order_number of the last order
    order_number = 1
    if orders:
        order_number = orders[list(orders.keys())[-1]]["order_number"] + 1

    data["order_number"] = order_number
    # create the order
    db.child("Orders").push(data)

    # send order object
    orders = db.child("Orders").get().val()
    # send the current order
    currentOrders = []
    for key, order in orders.items():
        order["id"] = key
        currentOrders.append(order)
    # SEND the latest order only
    currentOrders = currentOrders[-1]
    return JsonResponse({"status": "success", "orders": currentOrders})



@csrf_exempt
def get_orders(request, id):
    orders = db.child("Orders").order_by_child("user_id").equal_to(id).get().val()
    if not orders:
        return JsonResponse({"status": "error", "message": "Orders not found"})
    for key, order in orders.items():
        order["id"] = key
        for item in order["items"]:
            item["tiffin"] = db.child("Tiffins").child(item["id"]).get().val()
            order['business'] = db.child("Users").child(item["tiffin"]["business_id"]).get().val()
    orders = list(orders.values())
    return JsonResponse({"status": "success", "orders": orders})

@csrf_exempt
def getOrder(request, id):
    order = db.child("Orders").order_by_child("order_number").equal_to(id).get().val()
    if not order:
        return JsonResponse({"status": "error", "message": "Order not found"})
    order = list(order.values())[0]
    if not order:
        return JsonResponse({"status": "error", "message": "Order not found"})
    address = db.child("Addresses").child(order["address"]).get().val()
    # add urder id (key to the order object)
    order["id"] = list(order.keys())[0]
    return JsonResponse({"status": "success", "order": order})


@csrf_exempt
def getBusinessOrders(request, id):
    # find orders that has id in items for the tiffins o f this business
    business_tiffins = db.child("Tiffins").order_by_child("business_id").equal_to(id).get().val()
    if not business_tiffins:
        return JsonResponse({"status": "error", "message": "No tiffins found"})
    orders = []
    all_orders = db.child("Orders").get().val()
    if not all_orders:
        return JsonResponse({"status": "error", "message": "No orders found"})
    tiffin_ids = [tiffin["id"] for tiffin in business_tiffins.values()]
    # Iterate over all orders and check if any of the items match the tiffin ids
    for order_id, order in all_orders.items():
        for item in order["items"]:
            if item["id"] in tiffin_ids:
                order["id"] = order_id
                orders.append(order)
                order['user'] = db.child("Users").child(order['user_id']).get().val()
                order['tiffin'] = db.child("Tiffins").child(item["id"]).get().val()
                order['quantity'] = item["quantity"]
                break  # No need to check further items in this order
    if not orders:
        return JsonResponse({"status": "error", "message": "No orders found for this business"})
    return JsonResponse({"status": "success", "orders": orders})

@csrf_exempt


def update_order(request, id):
    data = json.loads(request.body)
    order = db.child("Orders").order_by_child("order_number").equal_to(id).get().val()
    order['id'] = list(order.keys())[0]
    if not order:
        return JsonResponse({"status": "error", "message": "Order not found"})
    order['order_status'] = data['order_status']
    db.child("Orders").child(order["id"]).update(order)
    order = db.child("Orders").order_by_child("order_number").equal_to(id).get().val()
    return JsonResponse({"status": "success", "order": order})


@csrf_exempt
def updateDeliveryInformation(request, id):
    data = json.loads(request.body)
    db.child("Orders").order_by_child("order_number").equal_to(id).update(data)
    order = db.child("Orders").child(id).get().val()
    if not order:
        return JsonResponse({"status": "error", "message": "Order not found"})
    return JsonResponse({"status": "success", "order": order})
