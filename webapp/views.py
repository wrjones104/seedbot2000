import requests 
import json     
import traceback
from datetime import datetime
from django.conf import settings 
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Count
from django.http import JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from allauth.socialaccount.models import SocialAccount
from celery.result import AsyncResult
from asgiref.sync import async_to_sync
import os
import uuid
from pathlib import Path

from seedbot_project.celery import app as celery_app

from bot import flag_builder
from bot.utils import flag_processor
from .models import Preset, UserPermission, FeaturedPreset, SeedLog, UserFavorite
from .forms import PresetForm, TuneUpForm
from .decorators import discord_login_required
from .tasks import create_local_seed_task, validate_preset_task, apply_tunes_task, create_api_seed_task
from bot.utils.metric_writer import write_gsheets
from bot.utils.tunes_processor import apply_tunes


def get_silly_things_list():
    try:
        file_path = settings.BASE_DIR / 'data' / 'silly_things_for_seedbot_to_say.txt'
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except FileNotFoundError:
        return ["Let's find some treasure!"]

def user_is_official(user_id):
    try:
        permissions = UserPermission.objects.get(user_id=user_id)
        return permissions.bot_admin == 1 or permissions.race_admin == 1
    except UserPermission.DoesNotExist:
        return False

def user_is_race_admin(user_id):
    try:
        permissions = UserPermission.objects.get(user_id=user_id)
        return permissions.race_admin == 1
    except UserPermission.DoesNotExist:
        return False

def home_view(request):
    """
    Renders the new home/landing page.
    """
    context = {
        'silly_things_json': json.dumps(get_silly_things_list()),
    }
    return render(request, 'webapp/home.html', context)

def tune_up_view(request):
    """
    Renders the Tune-Up page with the upload form.
    The actual processing is handled by tune_up_api_view.
    """
    form = TuneUpForm()
    context = {
        'form': form,
        'silly_things_json': json.dumps(get_silly_things_list()),
    }
    return render(request, 'webapp/tune_up.html', context)

@require_POST
def tune_up_api_view(request):
    """
    Handles the file upload from the Tune-Up form, saves the file temporarily,
    and dispatches a Celery task to process it.
    """
    form = TuneUpForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({'error': 'Invalid form submission. Please provide a ROM file.'}, status=400)

    uploaded_file = request.FILES['rom_file']
    tunes_type = request.POST.get('tunes_type')

    # --- Temporary File Handling ---
    temp_dir = Path(settings.MEDIA_ROOT) / 'temp_roms'
    temp_dir.mkdir(exist_ok=True)
    
    # Generate a unique filename to avoid conflicts
    unique_filename = f"{uuid.uuid4()}{Path(uploaded_file.name).suffix.lower()}"
    temp_file_path = temp_dir / unique_filename

    # Save the uploaded file to the temporary location
    try:
        with open(temp_file_path, 'wb+') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
    except IOError as e:
        return JsonResponse({'error': f'Failed to save uploaded file: {e}'}, status=500)

    # --- Dispatch Celery Task ---
    # Pass the path to the file, not the file object itself.
    task = apply_tunes_task.delay(str(temp_file_path), tunes_type)
    
    return JsonResponse({'task_id': task.id})

def tune_up_status_view(request, task_id):
    """
    Checks and returns the status of a tune-up Celery task.
    This is polled by the front-end JavaScript.
    """
    task_result = AsyncResult(task_id)
    response_data = {
        'task_id': task_id,
        'status': task_result.status,
        'result': None
    }

    if task_result.state == 'SUCCESS':
        response_data['result'] = task_result.result
    elif task_result.state == 'FAILURE':
        # Safely convert exception info to a string
        response_data['result'] = str(task_result.info)
    elif task_result.state == 'PROGRESS':
        response_data['result'] = task_result.info.get('status', 'Processing...')
    
    return JsonResponse(response_data)

def quick_roll_view(request):
    """
    Renders the Quick Roll page, fetching the relevant presets.
    """
    # Define all presets the page should look for
    QUICK_ROLL_MAPPING = {
        'rando': 'Quick Roll - Rando',
        'chaos': 'Quick Roll - Chaos',
        'true_chaos': 'Quick Roll - True Chaos',
        'worlds_divided': 'Worlds Divided',
        'practice_easy': 'Quick Roll - Practice Easy',
        'practice_medium': 'Quick Roll - Practice Medium',
        'practice_hard': 'Quick Roll - Practice Hard',
        'maps': 'Quick Roll - Maps',
        'doors': 'Quick Roll - Doors',
        'dungeon_crawl': 'Quick Roll - Dungeon Crawl',
    }

    # Fetch all the presets from the database in a single query
    presets_qs = Preset.objects.filter(preset_name__in=QUICK_ROLL_MAPPING.values())
    
    # Create a lookup dictionary for easier access
    presets_by_name = {p.preset_name: p for p in presets_qs}
    
    # Build the context dictionary for the template
    quick_rolls = {}
    for key, name in QUICK_ROLL_MAPPING.items():
        # Get the preset from the lookup, defaulting to None if not found
        quick_rolls[key] = presets_by_name.get(name)
    
    context = {
        'silly_things_json': json.dumps(get_silly_things_list()),
        'quick_rolls': quick_rolls
    }
    return render(request, 'webapp/quick_roll.html', context)

def preset_list_view(request):
    sort_key = request.GET.get('sort', '-count')
    order_by_field = {
        'name': 'preset_name', '-name': '-preset_name',
        'creator': 'creator_name', '-creator': '-creator_name',
        'count': 'gen_count', '-count': '-gen_count',
    }.get(sort_key, '-count')
    
    featured_preset_pks = list(FeaturedPreset.objects.values_list('preset_name', flat=True))
    
    user_favorites = []
    favorite_presets_list = Preset.objects.none()
    is_race_admin = False
    user_discord_id = None

    if request.user.is_authenticated:
        try:
            discord_account = request.user.socialaccount_set.get(provider='discord')
            user_discord_id = int(discord_account.uid)
            is_race_admin = user_is_race_admin(user_discord_id)
            
            user_favorites = list(UserFavorite.objects.filter(user_id=user_discord_id).values_list('preset_id', flat=True))
            favorite_presets_list = Preset.objects.filter(pk__in=user_favorites)

        except SocialAccount.DoesNotExist:
            pass

    exclude_pks = set(featured_preset_pks) | set(user_favorites)
    featured_presets = Preset.objects.filter(pk__in=featured_preset_pks).order_by(order_by_field)
    queryset = Preset.objects.exclude(pk__in=exclude_pks).exclude(preset_name='').order_by(order_by_field)
    
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(preset_name__icontains=query) |
            Q(description__icontains=query) |
            Q(creator_name__icontains=query)
        )

    context = {
        'featured_presets': featured_presets,
        'favorite_presets_list': favorite_presets_list,
        'presets': queryset,
        'search_query': query or '',
        'user_discord_id': user_discord_id,
        'silly_things_json': json.dumps(get_silly_things_list()),
        'current_sort': sort_key,
        'is_race_admin': is_race_admin,
        'user_favorites': user_favorites,
        'on_all_presets_page': True,
    }
    return render(request, 'webapp/preset_list.html', context)

def preset_detail_view(request, pk):
    preset = get_object_or_404(Preset, pk=pk)
    is_owner = False
    if request.user.is_authenticated:
        try:
            discord_id = request.user.socialaccount_set.get(provider='discord').uid
            if preset.creator_id == int(discord_id):
                is_owner = True
        except SocialAccount.DoesNotExist:
            pass

    silly_things = get_silly_things_list()
    silly_things_json = json.dumps(silly_things)
    back_url = request.META.get('HTTP_REFERER', '/')

    context = {
        'preset': preset,
        'is_owner': is_owner,
        'silly_things_json': silly_things_json,
        'back_url': back_url,
    }
    return render(request, 'webapp/preset_detail.html', context)

@discord_login_required
def my_profile_view(request):
    discord_account = request.user.socialaccount_set.get(provider='discord')
    discord_id = int(discord_account.uid)

    # Get all rolls and calculate stats
    user_rolls = SeedLog.objects.filter(creator_id=discord_id)
    total_rolls = user_rolls.count()
    favorite_preset_query = user_rolls.values('seed_type').annotate(roll_count=Count('seed_type')).order_by('-roll_count').first()
    
    # Implement custom sorting for timestamps since they are stored as strings
    def parse_timestamp(roll):
        try:
            return datetime.strptime(roll.timestamp, '%b %d %Y %H:%M:%S')
        except (ValueError, TypeError):
            # Return a very old date for any rolls with invalid timestamps
            return datetime.min

    # Convert queryset to a list and sort it in Python
    all_rolls_list = list(user_rolls)
    sorted_rolls = sorted(all_rolls_list, key=parse_timestamp, reverse=True)
    recent_rolls = sorted_rolls[:10] # Slice the sorted list

    # Get the user's created presets, with search and sort
    search_query = request.GET.get('q')
    sort_key = request.GET.get('sort', 'name')
    order_by_field = {'name': 'preset_name', '-count': '-gen_count'}.get(sort_key, 'preset_name')
    user_presets = Preset.objects.filter(creator_id=discord_id).order_by(order_by_field)
    if search_query:
        user_presets = user_presets.filter(Q(preset_name__icontains=search_query) | Q(description__icontains=search_query))

    # Get the user's favorited presets
    favorited_preset_pks = list(UserFavorite.objects.filter(user_id=discord_id).values_list('preset_id', flat=True))
    favorite_presets_list = Preset.objects.filter(pk__in=favorited_preset_pks)

    context = {
        'total_rolls': total_rolls,
        'favorite_preset': favorite_preset_query or "N/A",
        'recent_rolls': recent_rolls,
        'user_presets': user_presets,
        'favorite_presets_list': favorite_presets_list,
        'user_favorites': favorited_preset_pks,
        'search_query': search_query or '',
        'current_sort': sort_key,
        'user_discord_id': discord_id,
        'is_race_admin': user_is_race_admin(discord_id),
        'silly_things_json': json.dumps(get_silly_things_list()),
    }
    return render(request, 'webapp/my_profile.html', context)

def preset_status_view(request, pk):
    try:
        preset = Preset.objects.get(pk=pk)
        return JsonResponse({'status': preset.validation_status})
    except Preset.DoesNotExist:
        return JsonResponse({'status': 'DELETED'}, status=404)

@discord_login_required 
def preset_create_view(request):
    discord_account = request.user.socialaccount_set.get(provider='discord')
    is_official = user_is_official(discord_account.uid)
    if request.method == 'POST':
        form = PresetForm(request.POST, is_official=is_official)
        if form.is_valid():
            preset = form.save(commit=False)
            preset.creator_id = discord_account.uid
            preset.creator_name = discord_account.extra_data.get('username', request.user.username)
            preset.save()
            return redirect('my-profile')
    else:
        form = PresetForm(is_official=is_official)
    
    context = {'form': form, 'preset': None, 'silly_things_json': json.dumps(get_silly_things_list())}
    return render(request, 'webapp/preset_form.html', context)

@discord_login_required
def preset_update_view(request, pk):
    preset = get_object_or_404(Preset, pk=pk)
    discord_account = request.user.socialaccount_set.get(provider='discord')
    if preset.creator_id != int(discord_account.uid):
        raise PermissionDenied
    is_official = user_is_official(discord_account.uid)
    if request.method == 'POST':
        form = PresetForm(request.POST, instance=preset, is_official=is_official)
        if form.is_valid():
                preset = form.save()
        return redirect('preset-detail', pk=preset.pk)
    else:
        form = PresetForm(instance=preset, is_official=is_official)

    context = {'form': form, 'preset': preset, 'silly_things_json': json.dumps(get_silly_things_list())}
    return render(request, 'webapp/preset_form.html', context)

@discord_login_required
def preset_delete_view(request, pk):
    preset = get_object_or_404(Preset, pk=pk)
    discord_account = request.user.socialaccount_set.get(provider='discord')
    if preset.creator_id != int(discord_account.uid):
        raise PermissionDenied
    if request.method == 'POST':
        preset.delete()
        return redirect('my-profile')

    context = {'preset': preset, 'silly_things_json': json.dumps(get_silly_things_list())}
    return render(request, 'webapp/preset_confirm_delete.html', context)

@discord_login_required
def toggle_feature_view(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    discord_id = request.user.socialaccount_set.get(provider='discord').uid
    if not user_is_race_admin(discord_id):
         raise PermissionDenied("You do not have permission to feature presets.")

    preset = get_object_or_404(Preset, pk=pk)
    featured_obj, created = FeaturedPreset.objects.get_or_create(preset_name=preset.pk)
    
    if created:
        return JsonResponse({'status': 'success', 'featured': True})
    else:
        featured_obj.delete()
        return JsonResponse({'status': 'success', 'featured': False})
    
@discord_login_required
def toggle_favorite_view(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    discord_id = request.user.socialaccount_set.get(provider='discord').uid
    preset = get_object_or_404(Preset, pk=pk)

    try:
        favorite_obj, created = UserFavorite.objects.get_or_create(
            user_id=discord_id,
            preset=preset
        )
        
        if created:
            return JsonResponse({'status': 'success', 'favorited': True})
        else:
            favorite_obj.delete()
            return JsonResponse({'status': 'success', 'favorited': False})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def make_yaml_view(request, pk):
    preset = get_object_or_404(Preset, pk=pk)

    with open(os.path.join(settings.BASE_DIR, 'data', 'template.yaml'), 'r') as f:
        template_content = f.read()

    # Replace placeholders
    yaml_content = template_content.replace('flags', preset.flags)
    yaml_content = yaml_content.replace('ts_option', 'on_with_additional_gating')

    # Generate a filename
    filename = f"{preset.preset_name.replace(' ', '_')}.yaml"

    response = HttpResponse(yaml_content, content_type='application/x-yaml')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response

# Make sure this task is imported at the top of views.py
from .tasks import create_local_seed_task, create_api_seed_task

# Replace your existing view with this one
def roll_seed_dispatcher_view(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        preset = get_object_or_404(Preset, pk=pk)
        args_list = preset.arguments.split() if preset.arguments else []
        
        # Get user info for logging, which we'll pass to the task
        if request.user.is_authenticated:
            social_account = request.user.socialaccount_set.get(provider='discord')
            discord_id = int(social_account.uid)
            user_name = social_account.extra_data.get('username', request.user.username)
        else:
            discord_id = 0
            user_name = "Anonymous"

        # Define which arguments trigger a local roll.
        # Note: The dynamic flag logic for Rando/Chaos is now handled inside the Celery task.
        local_roll_args = ('practice', 'practice_easy', 'practice_medium', 'practice_hard', 'doors', 'dungeoncrawl', 'doorslite', 'doorx', 'maps', 'mapx', 'lg1', 'lg2', 'ws', 'csi', 'tunes', 'ctunes')

        # Decide which background task to run
        if any(arg in local_roll_args for arg in args_list):
            task = create_local_seed_task.delay(pk, discord_id, user_name)
        else:
            task = create_api_seed_task.delay(pk, discord_id, user_name)
        
        # Immediately return the task ID so the frontend can start polling
        return JsonResponse({'task_id': task.id})

    except Exception as e:
        # This will catch any errors during task dispatch and return them to the user
        traceback.print_exc()
        return JsonResponse({'error': f'An unexpected error occurred while starting the task: {e}'}, status=500)

def get_local_seed_roll_status_view(request, task_id):
    task_result = AsyncResult(task_id)
    response_data = {
        'task_id': task_id,
        'status': task_result.status,
        'result': None
    }

    if task_result.state == 'SUCCESS':
        response_data['result'] = task_result.result
    elif task_result.state == 'FAILURE':
        response_data['result'] = str(task_result.info)
    elif task_result.state == 'PROGRESS':
        response_data['result'] = task_result.info.get('status', 'Processing...')
    
    return JsonResponse(response_data)

@csrf_exempt 
@require_POST 
def update_sotw_preset_view(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != f'Bearer {settings.SOTW_API_KEY}':
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    data = json.loads(request.body)
    flags = data.get('flags')
    description = data.get('description')

    try:
        preset, created = Preset.objects.update_or_create(
            preset_name='SotW',
            defaults={'flags': flags, 'description': description}
        )
        return JsonResponse({'status': 'success', 'preset_name': preset.preset_name})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)