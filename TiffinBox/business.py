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
def get_business(request, id):
    business = db.child("Users").child(id).get().val()
    if not business:
        return JsonResponse({"status": "error", "message": "Business not found"})
    tiffins = db.child("Tiffins").order_by_child("business_id").equal_to(id).get().val()
    if not tiffins:
        business["tiffins"] = []
    else:
        for key, tiffin in tiffins.items():
            tiffin["id"] = key
        business["tiffins"] = list(tiffins.values())
    business["id"] = id
    address = db.child("Addresses").order_by_child("user_id").equal_to(id).get().val()
    if not address:
        business["address"] = []
    else:
        business["address"] = list(address.values())
    return JsonResponse({"status": "success", "business": business})