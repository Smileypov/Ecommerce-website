from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.models import CartItem
from store.models import Product

def checkout(request):
    """
    Handle the checkout process and simulated payment.
    """
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    cart_items = CartItem.objects.filter(session_id=session_id)

    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        # Get shipping data from form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipcode')

        # Create the Order record
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            city=city,
            zipcode=zipcode,
            paid=True # Simulated payment always succeeds
        )

        # Move items from Cart to OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            # Reduce stock
            product = item.product
            product.stock -= item.quantity
            product.save()

        # Clear the cart
        CartItem.objects.filter(session_id=session_id).delete()

        messages.success(request, "Your order has been placed successfully!")
        return redirect('orders:order_success', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total_price': sum(item.product.price * item.quantity for item in cart_items)
    })

def order_success(request, order_id):
    """
    Display the order confirmation page.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_success.html', {'order': order})
