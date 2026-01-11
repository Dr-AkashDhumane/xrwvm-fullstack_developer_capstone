from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
import logging

logger = logging.getLogger(__name__)

# ---------------------------
# Login view
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
            logger.error(f"Error during login: {e}")
            return JsonResponse({"status": "fail", "message": "Error processing request"})
    return JsonResponse({"status": "fail", "message": "Only POST method allowed"})


# ---------------------------
# Logout view
# ---------------------------
@csrf_exempt
def logout_user(request):
    if request.method in ["GET", "POST"]:
        logout(request)
        return JsonResponse({"status": "success", "userName": ""})
    return JsonResponse({"status": "fail", "message": "Only GET or POST methods allowed"})


# ---------------------------
# Registration view
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

            # Check if user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"userName": username, "error": "Already Registered"})

            # Create new user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            login(request, user)  # Automatically log in new user
            return JsonResponse({"userName": username, "status": "Authenticated"})

        except Exception as e:
            logger.error(f"Error during registration: {e}")
            return JsonResponse({"status": "fail", "message": "Error processing request"})
    return JsonResponse({"status": "fail", "message": "Only POST method allowed"})
