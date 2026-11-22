from .models import Cart

def cart_processor(request):
    """
    Exposes cart item count and active cart to all Django templates.
    """
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    elif request.session.session_key:
        cart = Cart.objects.filter(session_key=request.session.session_key).first()

    total_items = cart.total_items if cart else 0

    return {
        'global_cart': cart,
        'cart_item_count': total_items,
    }
