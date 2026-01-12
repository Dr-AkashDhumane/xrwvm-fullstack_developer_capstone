from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'djangoapp'

urlpatterns = [
    # ---------------------------
    # User endpoints
    # ---------------------------
    path('register', views.registration, name='registration'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),

    # ---------------------------
    # Car endpoints
    # ---------------------------
    path('get_cars', views.get_cars, name='getcars'),

    # ---------------------------
    # Dealer endpoints
    # ---------------------------
    path('get_dealers', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),

    # ---------------------------
    # Review submission
    # ---------------------------
    path('add_review', views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
