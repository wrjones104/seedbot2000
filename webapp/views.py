import requests 
import json     
import traceback
from datetime import datetime
from django.conf import settings 
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Count
from django.http import JsonResponse
from allauth.socialaccount.models import SocialAccount
from celery.result import AsyncResult
import os

from seedbot_project.celery import app as celery_app

from bot import flag_builder
from bot.utils import flag_processor
from .models import Preset, UserPermission, FeaturedPreset, SeedLog, UserFavorite
from .forms import PresetForm
from .decorators import discord_login_required
from .tasks import create_local_seed_task
from bot.utils.metric_writer import write_gsheets # Corrected from webapp import

from . import tasks


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
            saved_preset = form.save()
            return redirect('preset-detail', pk=saved_preset.pk)
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

def roll_seed_dispatcher_view(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    preset = get_object_or_404(Preset, pk=pk)
    args_list = preset.arguments.split() if preset.arguments else []
    
    local_roll_args = ('practice', 'doors', 'dungeoncrawl', 'doorslite', 'maps', 'mapx', 'lg1', 'lg2', 'ws', 'csi', 'tunes', 'ctunes')
    
    if request.user.is_authenticated:
        social_account = request.user.socialaccount_set.get(provider='discord')
        discord_id = int(social_account.uid)
        user_name = social_account.extra_data.get('username', request.user.username)
    else:
        discord_id = 0
        user_name = "Anonymous"

    if any(arg in local_roll_args for arg in args_list):
        task_result = celery_app.send_task(
            'webapp.tasks.create_local_seed_task',
            args=[pk, discord_id, user_name]
        )
        return JsonResponse({'method': 'local', 'task_id': task_result.id})
    else:
        try:
            api_url = "https://api.ff6worldscollide.com/api/seed"
            final_flags = flag_processor.apply_args(preset.flags, preset.arguments)
            payload = {"key": settings.WC_API_KEY, "flags": final_flags}
            headers = {"Content-Type": "application/json"}
            response = requests.post(api_url, data=json.dumps(payload), headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            seed_url = data.get('url')
            
            preset.gen_count += 1
            preset.save(update_fields=['gen_count'])

            timestamp = datetime.now().strftime('%b %d %Y %H:%M:%S')
            has_paint = 'paint' in preset.arguments.lower() if preset.arguments else False
            
            log_entry = {
                'creator_id': discord_id, 'creator_name': user_name,
                'seed_type': preset.preset_name, 'share_url': seed_url,
                'timestamp': timestamp, 'server_name': 'WebApp',
                'random_sprites': has_paint, 'server_id': None, 'channel_name': None, 'channel_id': None
            }
            SeedLog.objects.create(**log_entry)
            write_gsheets(log_entry)
            
            return JsonResponse({'method': 'api', 'seed_url': seed_url})
        except requests.exceptions.RequestException as e:
            error_message = "The FF6WC API returned an error. Please check your flags."
            return JsonResponse({'error': error_message}, status=400)

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