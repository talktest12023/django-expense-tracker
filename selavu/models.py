from django.db import models
from django.contrib.auth.models import User  # To link with User model


class Category(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    # Unique category name
    name = models.CharField(max_length=255, unique=True)
    # ✅ Assigns category to creator
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name  # Show category name in admin panel


class Expense(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)  # Link to Category model
    date = models.DateField()  # Stores date
    add_by = models.ForeignKey(
        User, on_delete=models.CASCADE)  # Links to User model
    description = models.TextField()  # Long text field for description
    # Number with 2 decimal places
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.category.name} - {self.amount} - {self.date}"
