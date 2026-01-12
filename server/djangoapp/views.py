from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate
import json
import logging

logger = logging.getLogger(__name__)

# ---------------------------
# User Login
# ---------------------------
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                return JsonResponse({"status": "fail", "message": "Invalid credentials"})
        except Exception as e:
            logger.error(f"Login error: {e}")
            return JsonResponse({"status": "fail", "message": "Error processing request"})
    return JsonResponse({"status": "fail", "message": "Only POST method allowed"})


# ---------------------------
# User Logout
# ---------------------------
@csrf_exempt
def logout_user(request):
    if request.method in ["GET", "POST"]:
        logout(request)
        return JsonResponse({"status": "success", "userName": ""})
    return JsonResponse({"status": "fail", "message": "Only GET or POST methods allowed"})


# ---------------------------
# User Registration
# ---------------------------
@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data['userName']
            password = data['password']
            first_name = data.get('firstName', '')
            last_name = data.get('lastName', '')
            email = data.get('email', '')

            if User.objects.filter(username=username).exists():
                return JsonResponse({"userName": username, "error": "Already Registered"})

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})

        except Exception as e:
            logger.error(f"Registration error: {e}")
            return JsonResponse({"status": "fail", "message": "Error processing request"})
    return JsonResponse({"status": "fail", "message": "Only POST method allowed"})


# ---------------------------
# Get all cars
# ---------------------------
def get_cars(request):
    try:
        # Populate DB if empty
        if CarMake.objects.count() == 0:
            print("CarMake table empty, populating database...")
            initiate()

        car_models = CarModel.objects.select_related('car_make')
        cars = [
            {
                "CarModel": cm.name,
                "CarMake": cm.car_make.name,
                "Type": cm.type,
                "Year": cm.year
            }
            for cm in car_models
        ]
        return JsonResponse({"CarModels": cars})
    except Exception as e:
        logger.error(f"Error fetching cars: {e}")
        return JsonResponse({"status": "fail", "message": "Error fetching cars"})
