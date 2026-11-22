from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm
from .models import UserProfile

def register_view(request):
    if request.user.is_authenticated:
        return redirect('shop:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Update created profile with extra fields
            profile = user.profile
            profile.phone_number = form.cleaned_data.get('phone_number', '')
            profile.city = form.cleaned_data.get('city', 'Kathmandu')
            profile.address_line = form.cleaned_data.get('address_line', '')
            profile.save()

            # If user completed a guest quiz stored in session, link it!
            if 'guest_hair_profile_id' in request.session:
                from quizzes.models import HairProfile
                try:
                    guest_profile = HairProfile.objects.get(id=request.session['guest_hair_profile_id'], user__isnull=True)
                    guest_profile.user = user
                    guest_profile.save()
                    del request.session['guest_hair_profile_id']
                except HairProfile.DoesNotExist:
                    pass

            login(request, user)
            messages.success(request, f"Welcome to CURLIQUE, {user.username}! Your curly journey begins here.")
            return redirect('shop:home')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form, 'title': 'Join CURLIQUE'})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('shop:home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Associate guest quiz if any
            if 'guest_hair_profile_id' in request.session:
                from quizzes.models import HairProfile
                try:
                    guest_profile = HairProfile.objects.get(id=request.session['guest_hair_profile_id'], user__isnull=True)
                    guest_profile.user = user
                    guest_profile.save()
                    del request.session['guest_hair_profile_id']
                except HairProfile.DoesNotExist:
                    pass

            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('shop:home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form, 'title': 'Login to CURLIQUE'})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out safely.")
    return redirect('shop:home')

@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    hair_profile = getattr(request.user, 'hair_profiles', None)
    latest_hair_profile = hair_profile.order_by('-created_at').first() if hair_profile else None
    recent_orders = request.user.orders.order_by('-created_at')[:5]

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'hair_profile': latest_hair_profile,
        'recent_orders': recent_orders,
        'title': 'My Curl Profile & Account'
    })

@login_required
def edit_profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            request.user.first_name = form.cleaned_data.get('first_name')
            request.user.last_name = form.cleaned_data.get('last_name')
            request.user.email = form.cleaned_data.get('email')
            request.user.save()
            messages.success(request, "Your profile information was updated successfully!")
            return redirect('accounts:profile')
    else:
        form = UserProfileUpdateForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'title': 'Edit Profile'
    })
