from django.shortcuts import render, get_object_or_404, redirect
from .models import Expense, Category
from .forms import ExpenseForm
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
# Create your views here.


def expenses(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())


@login_required
def add_expense(request):
    categories = Category.objects.all()  # ✅ Fetch all categories
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.add_by = request.user  # Assign the logged-in user
            expense.save()
            return redirect('expense_list')  # Redirect to expense list page
    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {'form': form, 'categories': categories})


def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'edit_expense.html', {'form': form, 'expense': expense})


def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    # ✅ Redirect to expense list after deleting
    return redirect('expense_list')


def expense_list(request):
    expenses = Expense.objects.filter(
        add_by=request.user)  # Show only user's expenses
    return render(request, 'expense_list.html', {'expenses': expenses})
