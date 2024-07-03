import json
import random

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

SERVICE_ACCOUNT_KEY_PATH = "config/serviceAccountKey.json"
if not firebase_admin._apps:
    credentials = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    firebase_admin.initialize_app(credentials)


@csrf_exempt
def login(request):
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")

    user = auth.sign_in_with_email_and_password(email, password)

    if user is None:
        return JsonResponse({"status": "error", "message": "Invalid credentials"})

    print(user)
    uid = user["localId"]
    custom_token = firebase_auth.create_custom_token(uid)
    return JsonResponse({"status": "success", "user": user, "customToken": custom_token.decode("utf-8")})


@csrf_exempt
def signup(request):
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phoneNumber")
    name = data.get("fullName")
    print(email, password, phone, name)

    user = auth.create_user_with_email_and_password(email, password)
    print(user)
    # create user in cloud firestore
    db.child("Users").child(user["localId"]).set({
        "email": email,
        "phone": phone,
        "name": name,
        "password": password,
        "id": user["localId"],
        "role": "client",
        "status": "active",
        "image": ""
    })
    return JsonResponse({"status": "success", "user": user})


# Create your views here.
def index(request):
    return JsonResponse({"message": "Hello, world!"})


def profile(request, id: str):
    user = db.child("Users").child(id).get().val()
    if user:
        return JsonResponse({"status": "success", "user": user})
    else:
        return JsonResponse({"status": "error", "message": "User not found"})


@csrf_exempt
def send_otp(request):
    phone_number = request.POST.get("phone")
    otp = ''.join(random.choices('0123456789', k=6))
    print(phone_number, otp)
    try:
        firebase.auth().sign_in_with_phone_number(phone_number, otp)
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
def verify_otp(request):
    phone_number = request.POST.get("phone")
    otp = request.POST.get("otp")
    print(phone_number, otp)
    try:
        firebase.auth().sign_in_with_phone_number(phone_number, otp)
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
def verify_phone_number(request):
    if request.method == 'POST':
        verification_id = request.POST.get('verificationId')
        sms_code = request.POST.get('smsCode')

        try:
            credential = auth.PhoneAuthProvider.credential(verification_id, sms_code)
            user = auth.get_user(credential)
            # Optionally, perform further actions with the authenticated user
            return JsonResponse({'success': True, 'message': 'Verification successful'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
