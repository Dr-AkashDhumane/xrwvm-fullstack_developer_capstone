from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review
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


# ---------------------------
# Get all dealerships (optionally filter by state)
# ---------------------------
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"
    
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# ---------------------------
# Get dealer details by dealer_id
# ---------------------------
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# ---------------------------
# Get dealer reviews with sentiment analysis
# ---------------------------
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        if reviews:
            for review_detail in reviews:
                sentiment = analyze_review_sentiments(review_detail['review'])
                review_detail['sentiment'] = sentiment
        
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# ---------------------------
# Submit a review to backend (authenticated users only)
# ---------------------------
@csrf_exempt
def add_review(request):
    if not request.user.is_anonymous:
        try:
            data = json.loads(request.body)
            response = post_review(data)
            if response:
                return JsonResponse({"status": 200, "message": "Review posted successfully", "response": response})
            else:
                return JsonResponse({"status": 500, "message": "Failed to post review"})
        except Exception as e:
            return JsonResponse({"status": 401, "message": f"Error in posting review: {str(e)}"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
