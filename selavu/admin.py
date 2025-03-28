from django.contrib import admin


# Register the Category model in Django Admin
from .models import Category, Expense  # Import your models

# Register both Category and Expense models in Django Admin
admin.site.register(Category)
admin.site.register(Expense)
