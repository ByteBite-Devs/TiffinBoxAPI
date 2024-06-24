import json
import random
from django.http import JsonResponse
import pyrebase
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def login(request):
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")
    print(email, password)
    user = auth.sign_in_with_email_and_password(email, password)
    print(user)
    return JsonResponse({"status": "success", "user": user})


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
    return JsonResponse({"status": "success", "user": user})


# Create your views here.
def index(request):
    return  JsonResponse({"message": "Hello, world!"})


@csrf_exempt
def send_otp(request):
    phone_number = request.POST.get("phone")
    otp = ''.join(random.choices('0123456789', k=6))
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
