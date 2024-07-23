import json
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
def loginWithGoogle(request):
    data = json.loads(request.body)
    email = data.get("email")
    phone = data.get("phoneNumber")
    name = data.get("fullName")
    id = data.get("googleId")
    photoUrl = data.get("profileImageUrl")
    existingUser = db.child("Users").child(id).get().val()

    if existingUser is None:
        try:
            user_data = {
                "email": email,
                "phone": phone,
                "name": name,
                "role": "client",
                "status": "active",
                "image": photoUrl
            }
            user = db.child("Users").child(id).set(user_data)
            return JsonResponse({"status": "success", "user": user})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "success", "user": existingUser})


@csrf_exempt
def signup(request):
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phoneNumber")
    name = data.get("fullName")

    try:
        user = auth.create_user_with_email_and_password(email, password)
        user_data = {
            "email": email,
            "phone": phone,
            "name": name,
            "role": "client",
            "status": "active",
            "image": ""
        }
        db.child("Users").child(user["localId"]).set(user_data)
        return JsonResponse({"status": "success", "user": user})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
def loginWithPhone(request):
    data = json.loads(request.body)
    phone = data.get("phoneNumber")
    name = data.get("fullName")
    email = data.get("email")
    id = data.get("id")
    photoUrl = data.get("profileImageUrl")

    existingUser = db.child("Users").child(id).get().val()

    if existingUser is None:
        try:
            user_data = {
                "email": email,
                "phone": phone,
                "name": name,
                "role": "client",
                "status": "active",
                "image": photoUrl
            }
            db.child("Users").child(id).set(user_data)
            user = db.child("Users").child(id).get().val()
            return JsonResponse({"status": "success", "user": user})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "success", "user": existingUser})


@csrf_exempt
def business_signup(request):
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phoneNumber")
    business_name = data.get("businessName")

    try:
        user = auth.create_user_with_email_and_password(email, password)
        user_data = {
            "email": email,
            "phone": phone,
            "business_name": business_name,
            "role": "business",
            "status": "active",
            "image": "",
            "name": '',
            "verified": False
        }
        user = db.child("Users").child(user["localId"]).set(user_data)
        return JsonResponse({"status": "success", "user": user})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})