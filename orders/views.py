from decimal import Decimal
import json
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import Cart, CartItem, Order, OrderItem, PaymentTransaction
from .forms import CheckoutForm
from .esewa import EsewaSandboxPayment
from shop.models import Product

def _get_cart(request, create=False):
    """
    Helper to fetch or create the Cart for authenticated or guest sessions.
    """
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if not cart and create:
            cart = Cart.objects.create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first()
        if not cart and create:
            cart = Cart.objects.create(session_key=session_key)
    return cart

def cart_view(request):
    """
    Renders shopping cart page with items, quantities, subtotal, and checkout CTA.
    """
    cart = _get_cart(request, create=False)
    items = cart.items.select_related('product').all() if cart else []
    subtotal = cart.subtotal if cart else Decimal('0.00')

    # Suggested products
    suggested_products = Product.objects.filter(is_available=True)[:4]

    return render(request, 'orders/cart.html', {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'suggested_products': suggested_products,
        'title': 'Shopping Cart — CURLIQUE'
    })

@require_POST
def add_to_cart_view(request):
    """
    Adds a product to the cart with specified quantity.
    """
    product_id = request.POST.get('product_id')
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1

    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = _get_cart(request, create=True)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    messages.success(request, f"Added '{product.name}' to your cart.")
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'orders:cart'
    return redirect(next_url)

@require_POST
def update_cart_view(request):
    """
    Updates the quantity of a specific cart item.
    """
    item_id = request.POST.get('item_id')
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1

    cart = _get_cart(request, create=False)
    if cart:
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        if quantity <= 0:
            cart_item.delete()
            messages.info(request, f"Removed '{cart_item.product.name}' from your cart.")
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"Updated quantity for '{cart_item.product.name}'.")

    return redirect('orders:cart')

@require_POST
def remove_from_cart_view(request):
    """
    Removes an item completely from the cart.
    """
    item_id = request.POST.get('item_id')
    cart = _get_cart(request, create=False)
    if cart:
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        product_name = cart_item.product.name
        cart_item.delete()
        messages.info(request, f"Removed '{product_name}' from your cart.")

    return redirect('orders:cart')

def checkout_view(request):
    """
    Processes checkout, calculates Nepal delivery fee, and creates order.
    """
    cart = _get_cart(request, create=False)
    if not cart or cart.total_items == 0:
        messages.warning(request, "Your cart is empty. Add products before proceeding to checkout.")
        return redirect('shop:product_list')

    subtotal = cart.subtotal

    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }
        if hasattr(request.user, 'profile'):
            initial_data.update({
                'phone': request.user.profile.phone_number,
                'city': request.user.profile.city,
                'delivery_address': request.user.profile.address_line,
            })

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user

            # Calculate Nepal delivery fee: NPR 100 within Valley, NPR 180 outside
            city_val = form.cleaned_data.get('city', 'Kathmandu')
            if city_val in ['Kathmandu', 'Lalitpur', 'Bhaktapur']:
                delivery_fee = Decimal('100.00')
            else:
                delivery_fee = Decimal('180.00')

            order.subtotal = subtotal
            order.delivery_fee = delivery_fee
            order.total_amount = subtotal + delivery_fee
            order.save()

            # Create Order Items and update product stock
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    product_brand=item.product.brand,
                    price=item.product.price,
                    quantity=item.quantity
                )
                # Decrement stock
                if item.product.stock >= item.quantity:
                    item.product.stock -= item.quantity
                    item.product.save()

            # Clear cart
            cart.items.all().delete()

            # Handle payment routing
            if order.payment_method == 'ESEWA':
                return redirect('orders:esewa_initiate', order_number=order.order_number)
            else:
                # Cash on Delivery
                order.payment_status = 'PENDING'
                order.order_status = 'PLACED'
                order.save()
                messages.success(request, f"Order #{order.order_number} confirmed with Cash on Delivery!")
                return redirect('orders:order_success', order_number=order.order_number)
    else:
        form = CheckoutForm(initial=initial_data)

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart,
        'subtotal': subtotal,
        'title': 'Checkout — Shipping & Payment'
    })

def esewa_initiate_view(request, order_number):
    """
    Renders the eSewa Sandbox checkout transition page with signed form fields.
    Also provides test sandbox simulator for instant testing.
    """
    order = get_object_or_404(Order, order_number=order_number)
    esewa_params = EsewaSandboxPayment.prepare_payment_form(order, request)

    # Save transaction record
    PaymentTransaction.objects.get_or_create(
        order=order,
        transaction_uuid=esewa_params['transaction_uuid'],
        defaults={
            'amount': order.total_amount,
            'provider': 'eSewa Sandbox v2',
            'status': 'PENDING'
        }
    )

    return render(request, 'orders/esewa_initiate.html', {
        'order': order,
        'esewa_params': esewa_params,
        'title': f"eSewa Sandbox Payment — Order #{order.order_number}"
    })

def esewa_success_view(request):
    """
    eSewa Sandbox payment verification endpoint.
    Verifies base64 encoded data parameter and HMAC-SHA256 signature.
    Never marks order as paid without successful verification.
    """
    encoded_data = request.GET.get('data')
    if not encoded_data:
        messages.error(request, "No transaction data received from eSewa.")
        return redirect('orders:esewa_failure')

    result = EsewaSandboxPayment.decode_and_verify_response(encoded_data)
    
    if result.get('success'):
        tx_uuid = result.get('transaction_uuid')
        # Format of tx_uuid is {order_number}-{timestamp}
        order_number = tx_uuid.split('-')[0] + '-' + tx_uuid.split('-')[1] + '-' + tx_uuid.split('-')[2]
        
        try:
            order = Order.objects.get(order_number=order_number)
            order.payment_status = 'PAID'
            order.order_status = 'PROCESSING'
            order.save()

            # Update PaymentTransaction
            tx = PaymentTransaction.objects.filter(transaction_uuid=tx_uuid).first()
            if tx:
                tx.status = 'PAID'
                tx.transaction_code = result.get('transaction_code', '')
                tx.raw_response = json.dumps(result.get('raw', {}))
                tx.is_verified = True
                tx.save()

            messages.success(request, f"Payment verified successfully via eSewa Sandbox! Order #{order.order_number} is being processed.")
            return redirect('orders:order_success', order_number=order.order_number)
        except Order.DoesNotExist:
            messages.error(request, "Associated order could not be located.")
            return redirect('shop:home')
    else:
        messages.error(request, "eSewa Sandbox payment verification failed or signature mismatch.")
        return redirect('orders:esewa_failure')

def esewa_failure_view(request):
    """
    Renders eSewa Sandbox failure page with options to retry or switch to COD.
    """
    return render(request, 'orders/esewa_failed.html', {
        'title': 'eSewa Payment Failed / Cancelled'
    })

def order_success_view(request, order_number):
    """
    Displays confirmed order details, delivery address, items and tracking status.
    """
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'orders/order_success.html', {
        'order': order,
        'title': f"Order Confirmed — #{order.order_number}"
    })

@login_required
def order_history_view(request):
    """
    Displays customer order history.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {
        'orders': orders,
        'title': 'My Order History — CURLIQUE'
    })

def order_detail_view(request, order_number):
    """
    Displays single order details.
    """
    if request.user.is_authenticated:
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
    else:
        order = get_object_or_404(Order, order_number=order_number)

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'title': f"Order Details #{order.order_number}"
    })
