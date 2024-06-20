import json
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

