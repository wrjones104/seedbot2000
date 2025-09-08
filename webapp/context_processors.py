from django.conf import settings

def google_analytics(request):
    """
    Adds the Google Tag Manager ID to the template context.
    """
    return {'GOOGLE_TAG_MANAGER_ID': settings.GOOGLE_TAG_MANAGER_ID}