from .models import HairProfile

def hair_profile_processor(request):
    """
    Exposes active hair profile to all Django templates.
    """
    profile = None
    if request.user.is_authenticated:
        profile = HairProfile.objects.filter(user=request.user).first()
    
    if not profile and 'guest_hair_profile_id' in request.session:
        profile = HairProfile.objects.filter(id=request.session['guest_hair_profile_id']).first()

    return {
        'active_hair_profile': profile,
    }
