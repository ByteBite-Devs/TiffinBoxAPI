import json
import jwt
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pyrebase

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


@csrf_exempt
def tiffins(request):
    tiffins = db.child("Tiffins").get().val()
    for key, tiffin in tiffins.items():
        tiffin["id"] = key
    tiffins = list(tiffins.values())
    return JsonResponse({"status": "success", "tiffins": tiffins})


@csrf_exempt
def tiffin(request, id):
    if request.method == "GET":
        tiffin = db.child("Tiffins").child(id).get().val()
        if not tiffin:
            return JsonResponse({"status": "error", "message": "Tiffin not found"})
        tiffin["id"] = id
        return JsonResponse({"status": "success", "tiffin": tiffin})
    else:
        data = json.loads(request.body)
        db.child("Tiffins").child(id).update(data)
        tiffin = db.child("Tiffins").child(id).get().val()
        return JsonResponse({"status": "success", "tiffin": tiffin})


@csrf_exempt
def add_tiffin(request):
    data = json.loads(request.body)
    db.child("Tiffins").push(data)
    tiffins = db.child("Tiffins").get().val()
    # update the id and ut svalue in the tiffin object in firebase if it id is already not preseen
    for key, tiffin in tiffins.items():
            tiffin["id"] = key
            db.child("Tiffins").child(key).update(tiffin)
    tiffins = db.child("Tiffins").get().val()
    tiffins = list(tiffins.values())
    return JsonResponse({"status": "success", "tiffins": tiffins})


def business_tiffins(request, id):
    tiffins = db.child("Tiffins").order_by_child("business_id").equal_to(id).get().val()
    if not tiffins:
        return JsonResponse({"status": "error", "message": "Tiffins not found"})
    for key,tiffin in tiffins.items():
        tiffin["id"] = key
    return JsonResponse({"status": "success", "tiffins": tiffins})


@csrf_exempt
def update_tiffin(request):
    data = json.loads(request.body)
    db.child("Tiffins").child(data["id"]).update(data)
    tiffin = db.child("Tiffins").child(data["id"]).get().val()
    return JsonResponse({"status": "success", "tiffin": tiffin})
