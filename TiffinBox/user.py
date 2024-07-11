import json

import firebase_admin
from django.contrib.auth.decorators import login_required
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
def profile(request, id):
    if request.method == "GET":
        return get_profile(request, id)
    else:
        return update_profile(request, id)


def update_profile(request, id):
    try:
        data = json.loads(request.body)
        db.child("Users").child(id).update(data)
        user = db.child("Users").child(id).get().val()
        return JsonResponse({"status": "success", "user": user})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

def get_profile(request, id):
    try:
        user = db.child("Users").child(id).get().val()
        if user:
            return JsonResponse({"status": "success", "user": user})
        else:
            return JsonResponse({"status": "error", "message": "User not found"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
def addresses(request, id):
    user = db.child("Users").child(id).get().val()
    if user:
        addresses = db.child("Addresses").order_by_child("user_id").equal_to(id).get().val()
        if not addresses:
            return JsonResponse({"status": "error", "message": "No addresses found"})
        return JsonResponse({"status": "success", "addresses": addresses})
    else:
        return JsonResponse({"status": "error", "message": "User not found"})

@csrf_exempt
def add_address(request):
    try:
        data = json.loads(request.body)
        db.child("Addresses").push(data)
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@csrf_exempt
def set_default_address(request, id):
    try:
        address = db.child("Addresses").child(id).get().val()
        user = db.child("Users").child(address["user_id"]).get().val()
        all_addresses = db.child("Addresses").order_by_child("user_id").equal_to(address["user_id"]).get().val()
        for key, addr in all_addresses.items():
            addr["is_default"] = False  # Set all addresses to non-default initially
            if key == id:
                addr["is_default"] = True  # Set the specific address to default

            # Update all addresses in the database
        for key, addr in all_addresses.items():
            db.child("Addresses").child(key).update(addr)

        all_addresses = db.child("Addresses").order_by_child("user_id").equal_to(address["user_id"]).get().val()
        print("All addresses: ", all_addresses)
        return JsonResponse({"status": "success", "address": address, "user": user})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
