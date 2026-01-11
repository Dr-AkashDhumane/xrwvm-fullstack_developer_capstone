"""
djangoproj URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Django API routes for login, logout, registration, etc.
    path('djangoapp/', include('djangoapp.urls')),

    # Home page
    path('', TemplateView.as_view(template_name="Home.html"), name='home'),

    # Static pages
    path('about/', TemplateView.as_view(template_name="About.html"), name='about'),
    path('contact/', TemplateView.as_view(template_name="Contact.html"), name='contact'),

    # React client-side rendered pages
    path('login/', TemplateView.as_view(template_name="index.html"), name='login'),
    path('register/', TemplateView.as_view(template_name="index.html"), name='register'),
]

# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
