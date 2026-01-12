from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'djangoapp'

urlpatterns = [
    # User registration
    path('register', views.registration, name='registration'),

    # User login
    path('login', views.login_user, name='login'),

    # User logout
    path('logout', views.logout_user, name='logout'),

    # Get all cars (CarMakes and CarModels)
    path('get_cars', views.get_cars, name='getcars'),

    # Placeholder paths for dealer reviews and add review (future)
    # path('dealer_reviews/<int:dealer_id>/', views.get_dealer_reviews, name='dealer_reviews'),
    # path('add_review/', views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
