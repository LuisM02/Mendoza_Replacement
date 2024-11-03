from datetime import timezone
from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("declined", "Declined"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description


class ProjectElement(models.Model):
    project = models.ForeignKey(
        Project, related_name="elements", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Material(models.Model):
    element = models.ForeignKey(
        ProjectElement, related_name="materials", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)
    price_per_qty = models.DecimalField(max_digits=10, decimal_places=2)
    markup_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def total_cost(self):
        return self.quantity * self.price_per_qty * (1 + self.markup_percentage / 100)

    def __str__(self):
        return self.name
