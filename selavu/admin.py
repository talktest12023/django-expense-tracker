from .models import Category, Expense
from django.contrib import admin
from django.db.models import Sum
from django.utils.timezone import now, timedelta
from rangefilter.filters import DateRangeFilter
from django.shortcuts import redirect
import json  # ✅ Import json for sending chart data

admin.site.site_header = "Expense Tracker"  # ✅ Change the header
admin.site.site_title = "Expense Dashboard"  # ✅ Change the index title
# Import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(add_by=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        form.base_fields['user'].disabled = True
        return form


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'category', 'add_by', 'date')
    list_filter = (('date', DateRangeFilter),)  # ✅ Date range filter

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(add_by=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.add_by = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['add_by'].initial = request.user
        form.base_fields['add_by'].disabled = True
        return form

    def changelist_view(self, request, extra_context=None):
        """ ✅ Set default date range for Expense View """
        if not request.GET.get('date__range__gte') and not request.GET.get('date__range__lte'):
            today = now().date()
            first_date = today.replace(day=27) if today.day >= 27 else (
                today.replace(day=1) - timedelta(days=1)).replace(day=27)
            last_date = (first_date + timedelta(days=31)).replace(day=26)

            query_string = f"date__range__gte={first_date}&date__range__lte={last_date}"
            return redirect(f"{request.path}?{query_string}")

        return super().changelist_view(request, extra_context)


class CategoryExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_spent')
    list_filter = (('expense__date', DateRangeFilter),)

    def total_spent(self, obj):
        """ ✅ Sum of expenses per category for the selected date range """
        request = getattr(self, 'request', None)
        if not request:
            return 0

        start_date = request.GET.get('expense__date__range__gte')
        end_date = request.GET.get('expense__date__range__lte')

        expenses = Expense.objects.filter(category=obj, add_by=request.user)

        if start_date and end_date:
            expenses = expenses.filter(
                date__gte=start_date, date__lte=end_date)
        else:
            today = now().date()
            first_date = today.replace(day=27) if today.day >= 27 else (
                today.replace(day=1) - timedelta(days=1)).replace(day=27)
            last_date = (first_date + timedelta(days=31)).replace(day=26)
            expenses = expenses.filter(
                date__gte=first_date, date__lte=last_date)

        total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        return float(total)  # ✅ Convert Decimal to float

    total_spent.short_description = "Total Spent"

    def get_queryset(self, request):
        self.request = request
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def changelist_view(self, request, extra_context=None):
        """ ✅ Set default date range for Category View & Show Total Spending with Pie Chart """
        if not request.GET.get('expense__date__range__gte') and not request.GET.get('expense__date__range__lte'):
            today = now().date()
            first_date = today.replace(day=27) if today.day >= 27 else (
                today.replace(day=1) - timedelta(days=1)).replace(day=27)
            last_date = (first_date + timedelta(days=31)).replace(day=26)

            query_string = f"expense__date__range__gte={first_date}&expense__date__range__lte={last_date}"
            return redirect(f"{request.path}?{query_string}")

        # ✅ Get total spending across all categories
        total_spending = Expense.objects.filter(
            add_by=request.user).aggregate(Sum('amount'))['amount__sum'] or 0

        # ✅ Get category-wise spending
        category_totals = Expense.objects.filter(add_by=request.user).values(
            'category__name').annotate(total=Sum('amount'))

        category_labels = [c['category__name'] for c in category_totals]
        # ✅ Convert Decimal to float
        category_values = [float(c['total']) for c in category_totals]

        extra_context = extra_context or {}
        extra_context['total_spending'] = total_spending  # ✅ Pass to template
        extra_context['category_labels'] = json.dumps(category_labels)
        extra_context['category_values'] = json.dumps(category_values)
        extra_context['chart_width'] = 400  # Adjust width
        extra_context['chart_height'] = 400  # Adjust height

        return super().changelist_view(request, extra_context)


# ✅ Register admin models
try:
    admin.site.unregister(Category)
except admin.sites.NotRegistered:
    pass

admin.site.register(Category, CategoryExpenseAdmin)
admin.site.register(Expense, ExpenseAdmin)
