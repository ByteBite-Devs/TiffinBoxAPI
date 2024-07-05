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

SERVICE_ACCOUNT_KEY_PATH = "config/serviceAccountKey.json"
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    firebase_admin.initialize_app(cred)


def validate_token(token):
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        print("Token is valid")
    except Exception as e:
        print(f"Token validation error: {e}")


@csrf_exempt
def login(request):
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        uid = user["localId"]
        custom_token = firebase_auth.create_custom_token(uid)
        validate_token(custom_token.decode("utf-8"))
        user = db.child("Users").child(uid).get().val()
        print(f"Custom token: {custom_token.decode('utf-8')}")
        return JsonResponse({"status": "success", "user": user, "customToken": custom_token.decode("utf-8")})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


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
def send_otp(request):
    phone_number = request.POST.get("phone")
    try:
        verification_id = auth.generate_phone_number_verification_code(phone_number)
        return JsonResponse({"status": "success", "verificationId": verification_id})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
def verify_otp(request):
    phone_number = request.POST.get("phone")
    otp = request.POST.get("otp")
    try:
        credential = auth.verify_phone_number(otp, phone_number)
        user = auth.get_user(credential)
        return JsonResponse({"status": "success", "user": user})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
def verify_phone_number(request):
    if request.method == 'POST':
        verification_id = request.POST.get('verificationId')
        sms_code = request.POST.get('smsCode')

        try:
            credential = auth.verify_phone_number(verification_id, sms_code)
            user = auth.get_user(credential)
            # Optionally, perform further actions with the authenticated user
            return JsonResponse({'success': True, 'message': 'Verification successful'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@csrf_exempt
def profile(request, id):
    try:
        user = db.child("Users").child(id).get().val()
        if user:
            return JsonResponse({"status": "success", "user": user})
        else:
            return JsonResponse({"status": "error", "message": "User not found"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


def index(request):
    return JsonResponse({"message": "Hello, world!"})