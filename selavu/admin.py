from .models import Category, Expense
from django.contrib import admin
from django.db.models import Sum
from django.utils.timezone import now, timedelta
import json  # ✅ Import json for sending chart data


admin.site.site_header = "Expense Tracker"  # ✅ Change the header
admin.site.site_title = "Expense Dashboard"  # ✅ Change the index title


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
    list_display = ('amount', 'category', 'add_by', 'description', 'date')
    # ✅ Uses a calendar picker
    # list_filter = (("date", DateRangePickerFilter),)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            qs = qs.filter(add_by=request.user)

        # ✅ Apply default filtering for the 27th of the previous month to the 26th of this month
        today = now().date()
        first_date = today.replace(day=27) if today.day >= 27 else (
            today.replace(day=1) - timedelta(days=1)).replace(day=27)
        last_date = (first_date + timedelta(days=31)).replace(day=26)

        return qs.filter(date__gte=first_date, date__lte=last_date)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.add_by = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['add_by'].initial = request.user
        form.base_fields['add_by'].disabled = True
        return form


class CategoryExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_spent')

    def total_spent(self, obj):
        """ ✅ Sum of expenses per category for the default date range """
        today = now().date()
        first_date = today.replace(day=27) if today.day >= 27 else (
            today.replace(day=1) - timedelta(days=1)).replace(day=27)
        last_date = (first_date + timedelta(days=31)).replace(day=26)

        expenses = Expense.objects.filter(
            category=obj, add_by=self.request.user,
            date__gte=first_date, date__lte=last_date
        )
        total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        return float(total)  # ✅ Convert Decimal to float

    total_spent.short_description = "Total Spent"

    def get_queryset(self, request):
        self.request = request
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def changelist_view(self, request, extra_context=None):
        """ ✅ Show Total Spending with Pie Chart """
        today = now().date()
        first_date = today.replace(day=27) if today.day >= 27 else (
            today.replace(day=1) - timedelta(days=1)).replace(day=27)
        last_date = (first_date + timedelta(days=31)).replace(day=26)

        # ✅ Get total spending across all categories
        total_spending = Expense.objects.filter(
            add_by=request.user, date__gte=first_date, date__lte=last_date
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        # ✅ Get category-wise spending
        category_totals = Expense.objects.filter(
            add_by=request.user, date__gte=first_date, date__lte=last_date
        ).values('category__name').annotate(total=Sum('amount'))

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
