from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import HairProfile
from .forms import CurlProfileQuizForm
from recommendations.engine import generate_hair_diagnosis
from shop.models import Product

def quiz_view(request):
    """
    Renders and processes the Curl Profile Quiz.
    Works for both logged-in users and guests.
    """
    existing_profile = None
    if request.user.is_authenticated:
        existing_profile = HairProfile.objects.filter(user=request.user).first()
    elif 'guest_hair_profile_id' in request.session:
        existing_profile = HairProfile.objects.filter(id=request.session['guest_hair_profile_id']).first()

    if request.method == 'POST':
        form = CurlProfileQuizForm(request.POST, instance=existing_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            if request.user.is_authenticated:
                profile.user = request.user
            else:
                if not request.session.session_key:
                    request.session.save()
                profile.session_key = request.session.session_key

            # Run rule-based diagnosis engine
            diagnosis = generate_hair_diagnosis(profile)
            profile.diagnosis_title = diagnosis['diagnosis_title']
            profile.diagnosis_summary = diagnosis['mp_balance']['headline']
            profile.save()

            if not request.user.is_authenticated:
                request.session['guest_hair_profile_id'] = profile.id

            messages.success(request, "Your Curl Profile has been generated successfully!")
            return redirect('quizzes:result', profile_id=profile.id)
    else:
        form = CurlProfileQuizForm(instance=existing_profile)

    return render(request, 'quizzes/quiz.html', {
        'form': form,
        'existing_profile': existing_profile,
        'title': 'Curl Profile Quiz — Find Your Pattern & Routine'
    })

def quiz_result_view(request, profile_id):
    """
    Displays the rule-based hair diagnosis, routine, and product recommendations.
    """
    profile = get_object_or_404(HairProfile, id=profile_id)
    
    # Run the rule-based diagnosis engine
    diagnosis = generate_hair_diagnosis(profile)

    # Fetch recommended catalogue products based on curl type, porosity, and budget
    all_products = Product.objects.filter(is_available=True)
    recommended_products = []

    for prod in all_products:
        # Rule filter: curl type in suitable_curl_types OR porosity in suitable_porosity
        curls = [c.strip() for c in prod.suitable_curl_types.split(',') if c.strip()]
        porosities = [p.strip().lower() for p in prod.suitable_porosity.split(',') if p.strip()]
        
        matches_curl = (profile.curl_type in curls or profile.curl_family in curls)
        matches_porosity = (profile.porosity in porosities)
        
        if matches_curl and matches_porosity:
            recommended_products.append(prod)

    # Fallback to featured products if exact filter is too narrow
    if not recommended_products:
        recommended_products = list(all_products[:4])

    return render(request, 'quizzes/quiz_result.html', {
        'profile': profile,
        'diagnosis': diagnosis,
        'recommended_products': recommended_products[:6],
        'title': f"Diagnosis: {diagnosis['diagnosis_title']}"
    })

def retake_quiz_view(request):
    """
    Allows user to retake the quiz to update their hair diagnosis.
    """
    return redirect('quizzes:quiz')
