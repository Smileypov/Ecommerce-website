from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from store.models import Product, Category
from orders.models import Order, OrderItem
from django.utils import timezone
from django.db.models import Sum, F

def is_admin(user):
    """
    Helper function to check if a user is a staff member.
    """
    return user.is_authenticated and user.is_staff

def admin_required(view_func):
    """
    Custom decorator for admin-only views.
    """
    from functools import wraps
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_admin(request.user):
            messages.error(request, "You do not have permission to access this page.")
            return redirect('admin_dashboard:admin_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_login(request):
    """
    Separate login view for administrative staff.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, "Welcome to the Admin Portal!")
            return redirect('admin_dashboard:dashboard')
        elif user is not None and not user.is_staff:
            messages.error(request, "Access denied. You are not a staff member.")
            return redirect('admin_dashboard:admin_login')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('admin_dashboard:admin_login')

    return render(request, 'admin_dashboard/admin_login.html')

def dashboard(request):
    """
    The main custom admin dashboard view.
    """
    if not is_admin(request.user):
        return redirect('admin_dashboard:admin_login')

    revenue_data = OrderItem.objects.aggregate(
        total=Sum(F('price') * F('quantity'))
    )
    total_revenue = revenue_data['total'] or 0

    context = {
        'total_orders': Order.objects.count(),
        'total_revenue': total_revenue,
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'recent_orders': Order.objects.order_by('-created')[:5],
    }
    return render(request, 'admin_dashboard/dashboard.html', context)
