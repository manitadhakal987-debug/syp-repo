from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category, SuitabilityTag, HaircutGuide
from quizzes.models import HairProfile
from recommendations.engine import evaluate_product_compatibility

def home_view(request):
    """
    Homepage of CURLIQUE Nepal.
    """
    featured_products = Product.objects.filter(is_available=True, is_featured=True)[:4]
    if not featured_products.exists():
        featured_products = Product.objects.filter(is_available=True)[:4]

    categories = Category.objects.all()
    haircut_guides = HaircutGuide.objects.all()[:3]

    # Fetch active user hair profile if available
    user_profile = None
    if request.user.is_authenticated:
        user_profile = HairProfile.objects.filter(user=request.user).first()
    elif 'guest_hair_profile_id' in request.session:
        user_profile = HairProfile.objects.filter(id=request.session['guest_hair_profile_id']).first()

    return render(request, 'shop/home.html', {
        'featured_products': featured_products,
        'categories': categories,
        'haircut_guides': haircut_guides,
        'user_profile': user_profile,
        'title': 'CURLIQUE — A Personalised Curly-Hair Care Platform for Nepal'
    })

def product_list_view(request):
    """
    Catalogue listing with dynamic search, category, curl type, porosity and budget filtering.
    """
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    tags = SuitabilityTag.objects.all()

    # Search Query
    q = request.GET.get('q', '').strip()
    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(brand__icontains=q) |
            Q(description__icontains=q) |
            Q(ingredients_list__icontains=q) |
            Q(key_actives__icontains=q)
        )

    # Category Filter
    category_slug = request.GET.get('category', '').strip()
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    # Curl Type Filter
    curl_filter = request.GET.get('curl', '').strip()
    if curl_filter:
        products = products.filter(suitable_curl_types__icontains=curl_filter)

    # Porosity Filter
    porosity_filter = request.GET.get('porosity', '').strip()
    if porosity_filter:
        products = products.filter(suitable_porosity__icontains=porosity_filter)

    # Tag Filter
    tag_slug = request.GET.get('tag', '').strip()
    if tag_slug:
        products = products.filter(suitability_tags__slug=tag_slug)

    # Budget Filter
    budget_filter = request.GET.get('budget', '').strip()
    if budget_filter == 'under_1000':
        products = products.filter(price__lt=1000)
    elif budget_filter == '1000_2500':
        products = products.filter(price__gte=1000, price__lte=2500)
    elif budget_filter == 'above_2500':
        products = products.filter(price__gt=2500)

    # Sorting
    sort_by = request.GET.get('sort', 'featured')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-is_featured', 'name')

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'tags': tags,
        'selected_category': selected_category,
        'current_q': q,
        'current_curl': curl_filter,
        'current_porosity': porosity_filter,
        'current_tag': tag_slug,
        'current_budget': budget_filter,
        'current_sort': sort_by,
        'title': 'Curly Hair Product Catalogue — Nepal'
    })

def product_detail_view(request, slug):
    """
    Product detail view with ingredient transparency and automated profile compatibility checker.
    """
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:3]

    # Check compatibility if user has a profile
    user_profile = None
    if request.user.is_authenticated:
        user_profile = HairProfile.objects.filter(user=request.user).first()
    elif 'guest_hair_profile_id' in request.session:
        user_profile = HairProfile.objects.filter(id=request.session['guest_hair_profile_id']).first()

    compatibility = None
    if user_profile:
        compatibility = evaluate_product_compatibility(product, user_profile)

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'user_profile': user_profile,
        'compatibility': compatibility,
        'title': f"{product.brand} - {product.name}"
    })

def haircut_guide_list_view(request):
    """
    Haircut Style Guide collection.
    """
    guides = HaircutGuide.objects.all().order_by('name')
    return render(request, 'shop/haircut_guide_list.html', {
        'guides': guides,
        'title': 'Curly Haircut Style Guide for Nepal Salons'
    })

def haircut_guide_detail_view(request, slug):
    """
    Detailed haircut guide with Nepali salon communication script.
    """
    guide = get_object_or_404(HaircutGuide, slug=slug)
    other_guides = HaircutGuide.objects.exclude(id=guide.id)[:3]
    return render(request, 'shop/haircut_guide_detail.html', {
        'guide': guide,
        'other_guides': other_guides,
        'title': f"Haircut Guide: {guide.name}"
    })
