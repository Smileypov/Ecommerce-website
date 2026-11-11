from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CartItem
from store.models import Product

def cart_detail(request):
    """
    Display items in the session-based shopping cart.
    """
    # Use session ID as a unique identifier for the cart
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    cart_items = CartItem.objects.filter(session_id=session_id)

    # Calculate totals
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    subtotal = total_price # In this simple version, no tax/shipping yet

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'subtotal': subtotal,
    }
    return render(request, 'cart/cart_detail.html', context)

def add_to_cart(request, product_id):
    """
    Add a product to the shopping cart.
    """
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)

        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        # Update quantity if product already exists in cart
        cart_item, created = CartItem.objects.get_or_create(
            session_id=session_id,
            product=product
        )

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        messages.success(request, f"Added {product.name} to your cart.")
        return redirect('store:product_detail', slug=product.slug)

    return redirect('store:product_list')

def remove_from_cart(request, product_id):
    """
    Remove a product from the shopping cart.
    """
    session_id = request.session.session_key
    if not session_id:
        return redirect('cart:cart_detail')

    CartItem.objects.filter(session_id=session_id, product_id=product_id).delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart:cart_detail')

def update_cart(request, product_id):
    """
    Update the quantity of an item in the cart.
    """
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            return redirect('cart:remove_from_cart', product_id=product_id)

        session_id = request.session.session_key
        if not session_id:
            return redirect('cart:cart_detail')

        CartItem.objects.filter(session_id=session_id, product_id=product_id).update(quantity=quantity)
        messages.success(request, "Cart updated.")

    return redirect('cart:cart_detail')
