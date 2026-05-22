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
from .models import UserPermission, FeaturedPreset, SeedLog, UserFavorite
from bot.utils.firestore_client import db, FirestorePresetAdapter, sanitize_preset_name
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

    # Fetch the mapping presets from Firestore
    presets_by_name = {}
    sanitized_ids = [sanitize_preset_name(name) for name in QUICK_ROLL_MAPPING.values()]
    doc_refs = [db.collection("presets").document(sid) for sid in sanitized_ids]
    if doc_refs:
        snaps = db.get_all(doc_refs)
        id_to_adapter = {s.id: FirestorePresetAdapter(s.to_dict()) for s in snaps if s.exists}
        for name in QUICK_ROLL_MAPPING.values():
            sid = sanitize_preset_name(name)
            if sid in id_to_adapter:
                presets_by_name[name] = id_to_adapter[sid]
    
    # Build the context dictionary for the template
    quick_rolls = {}
    for key, name in QUICK_ROLL_MAPPING.items():
        quick_rolls[key] = presets_by_name.get(name)
    
    context = {
        'silly_things_json': json.dumps(get_silly_things_list()),
        'quick_rolls': quick_rolls
    }
    return render(request, 'webapp/quick_roll.html', context)

def preset_list_view(request):
    sort_key = request.GET.get('sort', '-count')
    
    # Setup sorting key function
    sort_reverse = sort_key.startswith('-')
    raw_field = sort_key.lstrip('-')
    if raw_field == 'name':
        key_func = lambda p: p.preset_name.lower()
    elif raw_field == 'creator':
        key_func = lambda p: p.creator_name.lower()
    elif raw_field == 'count':
        key_func = lambda p: p.gen_count
    else:
        key_func = lambda p: p.gen_count
        sort_reverse = True

    featured_preset_pks = list(FeaturedPreset.objects.values_list('preset_name', flat=True))
    
    user_favorites = []
    is_race_admin = False
    user_discord_id = None

    if request.user.is_authenticated:
        try:
            discord_account = request.user.socialaccount_set.get(provider='discord')
            user_discord_id = int(discord_account.uid)
            is_race_admin = user_is_race_admin(user_discord_id)
            
            user_favorites = list(UserFavorite.objects.filter(user_id=user_discord_id).values_list('preset_name', flat=True))

        except SocialAccount.DoesNotExist:
            pass

    # Fetch only non-hidden presets from Firestore collection "presets"
    docs = db.collection("presets").where("hidden", "==", False).stream()
    visible_presets = [FirestorePresetAdapter(doc.to_dict()) for doc in docs if doc.to_dict().get("preset_name")]

    # Filter by search query if present
    query = request.GET.get('q')
    if query:
        query_lower = query.lower()
        visible_presets = [
            p for p in visible_presets if (
                query_lower in p.preset_name.lower() or
                query_lower in p.description.lower() or
                query_lower in p.creator_name.lower()
            )
        ]

    # Split into Featured, Favorites, and Others
    exclude_pks = set(featured_preset_pks) | set(user_favorites)
    
    featured_presets = [p for p in visible_presets if p.preset_name in featured_preset_pks]
    favorite_presets_list = [p for p in visible_presets if p.preset_name in user_favorites]
    queryset = [p for p in visible_presets if p.preset_name not in exclude_pks]

    # Sort each list
    featured_presets = sorted(featured_presets, key=key_func, reverse=sort_reverse)
    favorite_presets_list = sorted(favorite_presets_list, key=key_func, reverse=sort_reverse)
    queryset = sorted(queryset, key=key_func, reverse=sort_reverse)

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
    sanitized_id = sanitize_preset_name(pk)
    doc_snap = db.collection("presets").document(sanitized_id).get()
    if not doc_snap.exists:
        raise Http404("Preset not found")
    preset = FirestorePresetAdapter(doc_snap.to_dict())

    is_owner = False
    if request.user.is_authenticated:
        try:
            discord_id = request.user.socialaccount_set.get(provider='discord').uid
            if str(preset.creator_id) == str(discord_id):
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
    
    # Fetch from Firestore
    docs = db.collection("presets").where("creator_id", "==", str(discord_id)).get()
    user_presets = [FirestorePresetAdapter(doc.to_dict()) for doc in docs]
    
    # Filter by search in memory
    if search_query:
        search_query_lower = search_query.lower()
        user_presets = [
            p for p in user_presets if (
                search_query_lower in p.preset_name.lower() or
                search_query_lower in p.description.lower()
            )
        ]

    # Sort in memory
    sort_reverse = sort_key.startswith('-')
    raw_field = sort_key.lstrip('-')
    if raw_field == 'count':
        user_presets = sorted(user_presets, key=lambda p: p.gen_count, reverse=True) # Default gen_count is desc
    else:
        user_presets = sorted(user_presets, key=lambda p: p.preset_name.lower(), reverse=sort_reverse)

    # Get the user's favorited presets
    favorited_preset_pks = list(UserFavorite.objects.filter(user_id=discord_id).values_list('preset_name', flat=True))
    favorited_refs = [db.collection("presets").document(f_pk) for f_pk in favorited_preset_pks]
    if favorited_refs:
        f_snaps = db.get_all(favorited_refs)
        favorite_presets_list = [FirestorePresetAdapter(s.to_dict()) for s in f_snaps if s.exists]
            
    # Sort favorites by the same sort key
    if raw_field == 'count':
        favorite_presets_list = sorted(favorite_presets_list, key=lambda p: p.gen_count, reverse=True)
    else:
        favorite_presets_list = sorted(favorite_presets_list, key=lambda p: p.preset_name.lower(), reverse=sort_reverse)

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
        sanitized_id = sanitize_preset_name(pk)
        doc_snap = db.collection("presets").document(sanitized_id).get()
        if doc_snap.exists:
            status = doc_snap.to_dict().get('validation_status', 'PENDING')
            return JsonResponse({'status': status})
        else:
            return JsonResponse({'status': 'DELETED'}, status=404)
    except Exception:
        return JsonResponse({'status': 'DELETED'}, status=404)

@discord_login_required 
def preset_create_view(request):
    discord_account = request.user.socialaccount_set.get(provider='discord')
    is_official = user_is_official(discord_account.uid)
    if request.method == 'POST':
        form = PresetForm(request.POST, is_official=is_official)
        if form.is_valid():
            preset_name = form.cleaned_data['preset_name']
            base_sanitized = sanitize_preset_name(preset_name)
            sanitized_id = base_sanitized
            counter = 1
            while True:
                preset_name_lower = sanitized_id.lower()
                query = db.collection("presets").where("preset_name_lower", "==", preset_name_lower).limit(1).get()
                if not query:
                    break
                sanitized_id = f"{base_sanitized}-{counter}"
                counter += 1
            
            creator_id = str(discord_account.uid)
            creator_name = discord_account.extra_data.get('username', request.user.username)
            arguments = ' '.join(form.cleaned_data.get('arguments', []))
            doc_data = {
                "preset_name": sanitized_id,
                "preset_name_lower": sanitized_id.lower(),
                "creator_id": creator_id,
                "creator_name": creator_name,
                "created_at": datetime.now().strftime("%b %d %Y %H:%M:%S"),
                "flags": form.cleaned_data.get('flags', ''),
                "description": form.cleaned_data.get('description', ''),
                "arguments": arguments,
                "official": bool(form.cleaned_data.get('official', False)) if is_official else False,
                "hidden": bool(form.cleaned_data.get('hidden', False)),
                "gen_count": 0,
                "validation_status": 'PENDING',
                "validation_error": None
            }
            db.collection("presets").document(sanitized_id).set(doc_data)
            validate_preset_task.delay(sanitized_id)
            return redirect('my-profile')
    else:
        form = PresetForm(is_official=is_official)
    
    context = {'form': form, 'preset': None, 'silly_things_json': json.dumps(get_silly_things_list())}
    return render(request, 'webapp/preset_form.html', context)

@discord_login_required
def preset_update_view(request, pk):
    sanitized_id = sanitize_preset_name(pk)
    doc_ref = db.collection("presets").document(sanitized_id)
    doc_snap = doc_ref.get()
    if not doc_snap.exists:
        raise Http404("Preset not found")
    preset_data = doc_snap.to_dict()
    preset = FirestorePresetAdapter(preset_data)

    discord_account = request.user.socialaccount_set.get(provider='discord')
    if str(preset.creator_id) != str(discord_account.uid):
        raise PermissionDenied
    is_official = user_is_official(discord_account.uid)
    if request.method == 'POST':
        form = PresetForm(request.POST, instance=preset, is_official=is_official)
        if form.is_valid():
            arguments_str = ' '.join(form.cleaned_data.get('arguments', []))
            flags_changed = (form.cleaned_data.get('flags') != preset_data.get('flags'))
            args_changed = (arguments_str != preset_data.get('arguments'))
            
            update_data = {
                "description": form.cleaned_data.get('description', ''),
                "hidden": bool(form.cleaned_data.get('hidden', False))
            }
            if flags_changed or args_changed:
                update_data["flags"] = form.cleaned_data.get('flags', '')
                update_data["arguments"] = arguments_str
                update_data["validation_status"] = 'PENDING'
                update_data["validation_error"] = None
                
            if is_official:
                update_data["official"] = bool(form.cleaned_data.get('official', False))
                
            doc_ref.update(update_data)
            
            if flags_changed or args_changed:
                validate_preset_task.delay(sanitized_id)
                
            return redirect('preset-detail', pk=sanitized_id)
    else:
        form = PresetForm(instance=preset, is_official=is_official)

    context = {'form': form, 'preset': preset, 'silly_things_json': json.dumps(get_silly_things_list())}
    return render(request, 'webapp/preset_form.html', context)

@discord_login_required
def preset_delete_view(request, pk):
    sanitized_id = sanitize_preset_name(pk)
    doc_ref = db.collection("presets").document(sanitized_id)
    doc_snap = doc_ref.get()
    if not doc_snap.exists:
        raise Http404("Preset not found")
    preset_data = doc_snap.to_dict()
    preset = FirestorePresetAdapter(preset_data)

    discord_account = request.user.socialaccount_set.get(provider='discord')
    if str(preset.creator_id) != str(discord_account.uid):
        raise PermissionDenied
    if request.method == 'POST':
        doc_ref.delete()
        FeaturedPreset.objects.filter(preset_name=sanitized_id).delete()
        UserFavorite.objects.filter(preset_name=sanitized_id).delete()
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

    sanitized_id = sanitize_preset_name(pk)
    doc_snap = db.collection("presets").document(sanitized_id).get()
    if not doc_snap.exists:
        raise Http404("Preset not found")

    featured_obj, created = FeaturedPreset.objects.get_or_create(preset_name=sanitized_id)
    
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
    sanitized_id = sanitize_preset_name(pk)
    doc_snap = db.collection("presets").document(sanitized_id).get()
    if not doc_snap.exists:
        raise Http404("Preset not found")

    try:
        favorite_obj, created = UserFavorite.objects.get_or_create(
            user_id=discord_id,
            preset_name=sanitized_id
        )
        
        if created:
            return JsonResponse({'status': 'success', 'favorited': True})
        else:
            favorite_obj.delete()
            return JsonResponse({'status': 'success', 'favorited': False})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def make_yaml_view(request, pk):
    sanitized_id = sanitize_preset_name(pk)
    doc_snap = db.collection("presets").document(sanitized_id).get()
    if not doc_snap.exists:
        raise Http404("Preset not found")
    preset = FirestorePresetAdapter(doc_snap.to_dict())

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
        sanitized_id = sanitize_preset_name(pk)
        doc_snap = db.collection("presets").document(sanitized_id).get()
        if not doc_snap.exists:
            raise Http404("Preset not found")
        preset = FirestorePresetAdapter(doc_snap.to_dict())
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
        local_roll_args = ('practice', 'practice_easy', 'practice_medium', 'practice_hard', 'doors', 'dungeoncrawl', 'doorslite', 'doorx', 'maps', 'mapx', 'lg1', 'lg2', 'ws', 'csi', 'tunes', 'ctunes', 'dev', 'new')

        # Decide which background task to run
        if any(arg in local_roll_args for arg in args_list):
            task = create_local_seed_task.delay(sanitized_id, discord_id, user_name)
        else:
            task = create_api_seed_task.delay(sanitized_id, discord_id, user_name)
        
        # Immediately return the task ID so the frontend can start polling
        return JsonResponse({'task_id': task.id})

    except Exception as e:
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
        doc_ref = db.collection("presets").document("SotW")
        doc_data = {
            "preset_name": "SotW",
            "preset_name_lower": "sotw",
            "flags": flags,
            "description": description,
            "creator_id": "0",
            "creator_name": "System",
            "created_at": datetime.now().strftime("%b %d %Y %H:%M:%S"),
            "arguments": "",
            "official": True,
            "hidden": False,
            "validation_status": 'PENDING',
            "validation_error": None
        }
        doc_ref.set(doc_data)
        validate_preset_task.delay("SotW")
        return JsonResponse({'status': 'success', 'preset_name': 'SotW'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)