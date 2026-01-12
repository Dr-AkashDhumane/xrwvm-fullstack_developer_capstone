from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now

# -----------------------------
# Car Make Model
# -----------------------------
class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the car make, e.g., Toyota, Audi
    description = models.TextField(blank=True, null=True)  # Optional description
    founded_year = models.IntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(1800), MaxValueValidator(now().year)]
    )  # Optional field for founding year
    country = models.CharField(max_length=100, blank=True, null=True)  # Optional field for country

    def __str__(self):
        return self.name  # String representation shows the name of the make


# -----------------------------
# Car Model
# -----------------------------
class CarModel(models.Model):
    # Choices for car type
    SEDAN = 'SEDAN'
    SUV = 'SUV'
    WAGON = 'WAGON'
    COUPE = 'COUPE'
    HATCHBACK = 'HATCHBACK'
    CONVERTIBLE = 'CONVERTIBLE'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (COUPE, 'Coupe'),
        (HATCHBACK, 'Hatchback'),
        (CONVERTIBLE, 'Convertible'),
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')  # Many-to-One relation
    name = models.CharField(max_length=100)  # Model name, e.g., Camry, A6
    type = models.CharField(max_length=15, choices=CAR_TYPES, default=SEDAN)  # Type of car
    year = models.IntegerField(
        default=2023,
        validators=[MinValueValidator(2015), MaxValueValidator(2023)]
    )  # Year of manufacture
    dealership_id = models.IntegerField()  # ID of the dealer (from Cloudant or other DB)
    color = models.CharField(max_length=50, blank=True, null=True)  # Optional color field
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Optional price field

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
