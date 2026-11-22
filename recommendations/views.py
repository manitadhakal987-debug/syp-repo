from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from quizzes.models import HairProfile
from shop.models import Product, Category
from .engine import generate_hair_diagnosis, evaluate_product_compatibility
from .models import CurlCareRule

def routine_detail_view(request):
    """
    Renders the full, step-by-step personalized hair routine.
    """
    profile = None
    if request.user.is_authenticated:
        profile = HairProfile.objects.filter(user=request.user).first()
    elif 'guest_hair_profile_id' in request.session:
        profile = HairProfile.objects.filter(id=request.session['guest_hair_profile_id']).first()

    if not profile:
        messages.info(request, "Please take the quick Curl Profile Quiz first so we can tailor your routine!")
        return redirect('quizzes:quiz')

    diagnosis = generate_hair_diagnosis(profile)
    
    # Categorize catalogue products with clean identifiers
    step_products = {
        'cleanse': Product.objects.filter(category__slug='cleansers-shampoos', is_available=True)[:3],
        'condition': Product.objects.filter(category__slug='conditioners-deep-masks', is_available=True)[:3],
        'leave_in': Product.objects.filter(category__slug='leave-in-creams', is_available=True)[:3],
        'define': Product.objects.filter(category__slug='styling-gels-custards', is_available=True)[:3],
        'protect': Product.objects.filter(category__slug='accessories-tools', is_available=True)[:3],
    }

    return render(request, 'recommendations/routine_detail.html', {
        'profile': profile,
        'diagnosis': diagnosis,
        'step_products': step_products,
        'title': f"My Routine — {diagnosis['diagnosis_title']}"
    })

def compatibility_checker_view(request):
    """
    Evaluates whether any catalogue product is compatible with the user's hair profile.
    Only checks products in the catalogue (no pasted ingredient lists, complying strictly with requirements).
    """
    profile = None
    if request.user.is_authenticated:
        profile = HairProfile.objects.filter(user=request.user).first()
    elif 'guest_hair_profile_id' in request.session:
        profile = HairProfile.objects.filter(id=request.session['guest_hair_profile_id']).first()

    products = Product.objects.filter(is_available=True).order_by('brand', 'name')
    selected_product = None
    compatibility_result = None

    product_id = request.GET.get('product_id')
    if product_id:
        selected_product = get_object_or_404(Product, id=product_id)
        if profile:
            compatibility_result = evaluate_product_compatibility(selected_product, profile)

    return render(request, 'recommendations/compatibility_checker.html', {
        'profile': profile,
        'products': products,
        'selected_product': selected_product,
        'compatibility_result': compatibility_result,
        'title': 'Product Compatibility Checker'
    })
