import json
import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from celery.result import AsyncResult

from .models import APIKey, Preset
from .tasks import create_api_seed_generation_task
from bot import flag_builder

def require_api_key(view_func):
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({'error': 'Missing Authorization Header'}, status=401)

        try:
            # Expecting "Bearer <key>"
            scheme, key = auth_header.split()
            if scheme.lower() != 'bearer':
                return JsonResponse({'error': 'Invalid Authorization Scheme'}, status=401)
        except ValueError:
            return JsonResponse({'error': 'Invalid Authorization Header'}, status=401)

        try:
            api_key = APIKey.objects.get(key=key)
            now = timezone.now()
            # To avoid DB writes on every request, only update last_used if it's been a while.
            if not api_key.last_used or (now - api_key.last_used).total_seconds() > 60:
                api_key.last_used = now
                api_key.save(update_fields=['last_used'])
            request.api_key_user = api_key.user
        except APIKey.DoesNotExist:
            return JsonResponse({'error': 'Invalid API Key'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(require_api_key, name='dispatch')
class SeedGenerateAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        seed_type = data.get('type')
        if not seed_type:
            return JsonResponse({'error': 'Missing seed type'}, status=400)

        flags = None
        preset_name = None

        # User args can be a list or a string
        raw_args = data.get('args', [])
        if isinstance(raw_args, str):
            raw_args = raw_args.split()

        # Prepend hyphen if missing to standardize args
        user_args = []
        for arg in raw_args:
            if not arg.startswith('-'):
                user_args.append(f'-{arg}')
            else:
                user_args.append(arg)

        # Handle different seed types
        if seed_type == 'preset':
            preset_name = data.get('preset')
            if not preset_name:
                return JsonResponse({'error': 'Missing preset name'}, status=400)
            try:
                preset = Preset.objects.get(preset_name=preset_name)
                flags = preset.flags
                preset_args = preset.arguments.split() if preset.arguments else []
                # Append user args to preset args
                user_args = preset_args + user_args
            except Preset.DoesNotExist:
                return JsonResponse({'error': f'Preset "{preset_name}" not found'}, status=404)

        elif seed_type in ['custom', 'flagset', 'flags']:
            flags = data.get('flags')
            if not flags:
                return JsonResponse({'error': 'Missing flags for custom seed'}, status=400)
            preset_name = "API - Custom"

        elif seed_type == 'standard':
            flags = flag_builder.standard()
            preset_name = "API - Standard"

        elif seed_type == 'chaos':
            flags = flag_builder.chaos()
            preset_name = "API - Chaos"

        elif seed_type == 'true_chaos':
            flags = flag_builder.true_chaos()
            preset_name = "API - True Chaos"

        else:
             return JsonResponse({'error': f'Unknown seed type: {seed_type}'}, status=400)

        # Get user info from API Key
        user = request.api_key_user
        try:
            discord_account = user.socialaccount_set.get(provider='discord')
            creator_id = int(discord_account.uid)
            creator_name = discord_account.extra_data.get('username', user.username)
        except user.socialaccount_set.model.DoesNotExist:
             creator_id = 0
             creator_name = user.username

        # Dispatch task
        task = create_api_seed_generation_task.delay(
            flags=flags,
            args_list=user_args,
            seed_type_name=preset_name,
            creator_id=creator_id,
            creator_name=creator_name
        )

        return JsonResponse({
            'task_id': task.id,
            'status_url': request.build_absolute_uri(f'/api/v1/seed/status/{task.id}/')
        })

@method_decorator(require_api_key, name='dispatch')
class SeedStatusAPIView(View):
    def get(self, request, task_id):
        task_result = AsyncResult(task_id)

        # Check if the task result is ready even if status says something else,
        # though usually Celery state management is reliable if backend is configured correctly.
        # In some configurations, custom states like PROGRESS might persist if not overwritten.

        status = task_result.status
        response_data = {
            'task_id': task_id,
            'status': status,
        }

        if status == 'SUCCESS':
            share_url = task_result.result
            if share_url and share_url.startswith('/'):
                full_share_url = request.build_absolute_uri(share_url)
            else:
                full_share_url = share_url

            response_data['result_url'] = full_share_url
            response_data['download_url'] = request.build_absolute_uri(f'/api/v1/seed/{task_id}/download')

        elif status == 'FAILURE':
            response_data['error'] = str(task_result.info)

        elif status == 'PROGRESS':
            response_data['progress'] = task_result.info.get('status', 'Processing...')

        return JsonResponse(response_data)

@method_decorator(require_api_key, name='dispatch')
class SeedDownloadAPIView(View):
    def get(self, request, task_id):
        task_result = AsyncResult(task_id)
        if task_result.state != 'SUCCESS':
             return JsonResponse({'error': 'Task not completed successfully'}, status=400)

        share_url = task_result.result
        # share_url is typically /media/preset_....zip

        media_url = settings.MEDIA_URL
        if share_url and share_url.startswith(media_url):
            relative_path = share_url[len(media_url):]
            file_path = os.path.join(settings.MEDIA_ROOT, relative_path)

            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='application/zip')
                    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                    return response
            else:
                return JsonResponse({'error': 'File not found'}, status=404)
        else:
             return JsonResponse({'error': 'Invalid file path'}, status=500)
