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
def add_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        db.child("Reviews").push(data)
#         update teh average rating for the tiffin
        tiffin = db.child("Tiffins").child(data["tiffin_id"]).get().val()
        reviews = db.child("Reviews").order_by_child("tiffin_id").equal_to(data["tiffin_id"]).get().val()
        total_rating = 0
        for review in reviews.values():
            total_rating += review["rating"]
        average_rating = total_rating / len(reviews)
        db.child("Tiffins").child(data["tiffin_id"]).update({"average_rating": average_rating})
        db.child("Tiffins").child(data["tiffin_id"]).update({"reviews": len(reviews)})
        tiffin = db.child("Tiffins").child(data["tiffin_id"]).get().val()
        return JsonResponse({"status": "success", "tiffin": tiffin})


def get_reviews(request, id):
    reviews = db.child("Reviews").order_by_child("tiffin_id").equal_to(id).get().val()
    return JsonResponse({"status": "success", "reviews": reviews})

@csrf_exempt
def update_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        db.child("Reviews").child(data["id"]).update(data)
        review = db.child("Reviews").child(data["id"]).get().val()
        return JsonResponse({"status": "success", "review": review})


@csrf_exempt
def delete_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        db.child("Reviews").child(data["id"]).remove()
        return JsonResponse({"status": "success"})