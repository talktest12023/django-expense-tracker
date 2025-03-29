from django.urls import path
from . import views
from .views import create_admin, backup_db_view

urlpatterns = [
    path('expenses/',  views.expense_list, name='expense_list'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('edit-expense/<int:pk>/', views.edit_expense,
         name='edit_expense'),  # ✅ Ensure this line exists
    path('delete-expense/<int:pk>/', views.delete_expense,
         name='delete_expense'),  # ✅ Add this line
    path('create-admin/', create_admin),
    path('backup-db/', backup_db_view, name='backup-db'),
]
