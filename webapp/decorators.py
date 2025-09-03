from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse # <-- Add this import
from allauth.socialaccount.models import SocialAccount

def discord_login_required(view_func):
    """
    Decorator for views that checks that the user is logged in AND
    has a connected Discord account.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = reverse('account_login')
            redirect_url = f"{login_url}?next={request.path}"
            return redirect(redirect_url)
        # -----------------------------
        
        try:
            SocialAccount.objects.get(user=request.user, provider='discord')
        except SocialAccount.DoesNotExist:
            return redirect('connect-discord')
            
        return view_func(request, *args, **kwargs)

    return _wrapped_view