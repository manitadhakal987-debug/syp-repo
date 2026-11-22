import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'curlique.settings')
django.setup()

from django.test import Client
from shop.models import Product, HaircutGuide
from orders.models import Order
import json, base64

def run_tests():
    c = Client()
    print("--- 1. Testing Homepage ---")
    resp = c.get('/')
    assert resp.status_code == 200, f"Home failed: {resp.status_code}"
    assert b'CURLIQUE' in resp.content
    print("✓ Home page loaded (200 OK)")

    print("--- 2. Testing Product Catalogue & Filters ---")
    resp = c.get('/products/')
    assert resp.status_code == 200, f"Product list failed: {resp.status_code}"
    resp_filter = c.get('/products/?curl=3B&porosity=high')
    assert resp_filter.status_code == 200
    resp_search = c.get('/products/?q=Shea')
    assert resp_search.status_code == 200
    print("✓ Product Catalogue and filters working (200 OK)")

    print("--- 3. Testing Product Detail ---")
    product = Product.objects.first()
    assert product is not None
    resp = c.get(f'/product/{product.slug}/')
    assert resp.status_code == 200
    assert product.name.encode('utf-8') in resp.content
    print(f"✓ Product detail for '{product.name}' loaded (200 OK)")

    print("--- 4. Testing Haircut Style Guide ---")
    resp = c.get('/haircut-guide/')
    assert resp.status_code == 200
    guide = HaircutGuide.objects.first()
    assert guide is not None
    resp = c.get(f'/haircut-guide/{guide.slug}/')
    assert resp.status_code == 200
    assert b'What to Tell Your Hairstylist in Nepal' in resp.content
    print(f"✓ Haircut guide for '{guide.name}' loaded (200 OK)")

    print("--- 5. Testing Curl Profile Quiz Submission ---")
    quiz_data = {
        'curl_type': '3B',
        'porosity': 'high',
        'density': 'medium',
        'scalp_type': 'normal',
        'concerns': ['frizz', 'dryness'],
        'budget': 'mid',
    }
    resp = c.post('/quiz/', data=quiz_data)
    assert resp.status_code == 302, f"Quiz post failed: {resp.status_code}"
    redirect_url = resp.url
    print(f"✓ Quiz submission redirected to {redirect_url}")
    resp_res = c.get(redirect_url)
    assert resp_res.status_code == 200
    assert b'Rule-Based Diagnosis' in resp_res.content
    print("✓ Diagnosis & routine result page loaded (200 OK)")

    print("--- 6. Testing Routine Guide & Compatibility Checker ---")
    resp = c.get('/recommendations/routine/')
    assert resp.status_code == 200
    assert b'Your 5-Step Personalized Curly Routine' in resp.content or b'Routine' in resp.content
    print("✓ Routine guide loaded (200 OK)")

    resp = c.get(f'/recommendations/compatibility/?product_id={product.id}')
    assert resp.status_code == 200
    assert b'Product Compatibility Checker' in resp.content
    assert b'Match' in resp.content or b'Score' in resp.content or b'Compatible' in resp.content
    print(f"✓ Compatibility analysis for '{product.name}' passed (200 OK)")

    print("--- 7. Testing Cart & Checkout with Cash on Delivery ---")
    resp = c.post('/orders/cart/add/', data={'product_id': product.id, 'quantity': 2})
    assert resp.status_code == 302
    resp = c.get('/orders/cart/')
    assert resp.status_code == 200
    assert b'Shopping Cart' in resp.content
    print("✓ Product added to cart and cart page loaded (200 OK)")

    checkout_data = {
        'full_name': 'Bikash Adhikari',
        'email': 'bikash@example.com',
        'phone': '9801234567',
        'city': 'Kathmandu',
        'delivery_address': 'Baneshwor, Kathmandu',
        'order_notes': 'Please call before arrival',
        'payment_method': 'COD',
    }
    resp = c.post('/orders/checkout/', data=checkout_data)
    assert resp.status_code == 302, f"Checkout failed: {resp.status_code}"
    order_success_url = resp.url
    print(f"✓ COD Order placed, redirect: {order_success_url}")
    resp_success = c.get(order_success_url)
    assert resp_success.status_code == 200
    assert b'Order Confirmed' in resp_success.content
    print("✓ Order success confirmation page loaded (200 OK)")

    print("--- 8. Testing eSewa Sandbox Integration & Verification ---")
    # Add product to cart again
    c.post('/orders/cart/add/', data={'product_id': product.id, 'quantity': 1})
    esewa_checkout_data = {
        'full_name': 'Bikash Adhikari',
        'email': 'bikash@example.com',
        'phone': '9801234567',
        'city': 'Pokhara',
        'delivery_address': 'Lakeside, Ward 6',
        'order_notes': 'Deliver during office hours',
        'payment_method': 'ESEWA',
    }
    resp = c.post('/orders/checkout/', data=esewa_checkout_data)
    assert resp.status_code == 302
    esewa_init_url = resp.url
    print(f"✓ eSewa checkout redirected to: {esewa_init_url}")
    resp_init = c.get(esewa_init_url)
    assert resp_init.status_code == 200
    assert b'eSewa epay Sandbox v2' in resp_init.content

    # Extract transaction parameters from initiated order
    order_num = esewa_init_url.rstrip('/').split('/')[-1]
    order_obj = Order.objects.get(order_number=order_num)
    tx = order_obj.payments.first()
    assert tx is not None
    tx_uuid = tx.transaction_uuid

    from orders.esewa import EsewaSandboxPayment
    total_str = f"{order_obj.total_amount:.2f}"
    sig = EsewaSandboxPayment.generate_signature(total_str, tx_uuid)

    payload = {
        "transaction_code": "ESEWA-SIM-00123",
        "status": "COMPLETE",
        "total_amount": total_str,
        "transaction_uuid": tx_uuid,
        "product_code": "EPAYTEST",
        "signed_field_names": "total_amount,transaction_uuid,product_code",
        "signature": sig
    }
    encoded_b64 = base64.b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')
    resp_verify = c.get(f'/orders/esewa/success/?data={encoded_b64}')
    assert resp_verify.status_code == 302, f"Verification redirect failed: {resp_verify.status_code}"
    print(f"✓ eSewa payment verified successfully, redirect: {resp_verify.url}")

    # Check order status in DB
    updated_order = Order.objects.get(order_number=order_num)
    assert updated_order.payment_status == 'PAID'
    assert updated_order.order_status == 'PROCESSING'
    print(f"✓ Order #{order_num} verified and marked as PAID in database!")

    print("--- 9. Testing User Authentication & Profile ---")
    login_success = c.login(username='aarav', password='CurlyPass123!')
    assert login_success, "Login failed for aarav"
    resp = c.get('/accounts/profile/')
    assert resp.status_code == 200
    assert b'Aarav Shrestha' in resp.content
    print("✓ User profile page loaded for logged-in user (200 OK)")

    print("--- 10. Testing Admin Reports ---")
    c.login(username='admin', password='Admin1234!')
    resp = c.get('/admin/orders/order/dashboard-reports/')
    assert resp.status_code == 200
    assert b'CURLIQUE Analytics' in resp.content
    print("✓ Admin analytics & popular products report loaded (200 OK)")

    print("\n========================================================")
    print("🎉 ALL 10 TEST SUITES PASSED FLAWLESSLY WITH 100% SUCCESS!")
    print("========================================================")

if __name__ == '__main__':
    run_tests()
