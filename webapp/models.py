from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

class Preset(models.Model):
    VALIDATION_CHOICES = [
        ('PENDING', 'Pending'),
        ('VALID', 'Valid'),
        ('INVALID', 'Invalid'),
    ]

    preset_name = models.CharField(max_length=255, primary_key=True)
    creator_id = models.BigIntegerField()
    creator_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True, blank=True)
    flags = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    arguments = models.TextField(blank=True, null=True)
    official = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    gen_count = models.IntegerField(default=0)
    validation_status = models.CharField(max_length=10, choices=VALIDATION_CHOICES, default='PENDING')
    validation_error = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'presets'

class UserPermission(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    bot_admin = models.IntegerField()
    git_user = models.IntegerField()
    race_admin = models.IntegerField()
    class Meta:
        db_table = 'users'

import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def parse_timestamp(ts):
    if not ts:
        return None
    if isinstance(ts, datetime):
        return ts if ts.tzinfo is not None else ts.replace(tzinfo=timezone.utc)
    try:
        if isinstance(ts, str):
            ts = ts.strip()
            if ts.endswith('Z'):
                try:
                    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                except ValueError:
                    pass
            for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%b %d %Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
                try:
                    return datetime.strptime(ts, fmt).replace(tzinfo=timezone.utc)
                except ValueError:
                    pass
            val = datetime.fromisoformat(ts)
            return val if val.tzinfo is not None else val.replace(tzinfo=timezone.utc)
    except Exception:
        pass
    return ts

class FirestoreSeedLogAdapter:
    def __init__(self, data: dict, doc_id: str = None):
        self.doc_id = doc_id or str(data.get("id", ""))
        self.id = int(data.get("id") or doc_id or 0)
        self.creator_id = int(data.get("creator_id") or 0)
        self.creator_name = data.get("creator_name", "")
        self.seed_type = data.get("seed_type", "")
        self.share_url = data.get("share_url", "")
        
        ts_val = data.get("timestamp")
        self.timestamp = parse_timestamp(ts_val)
        
        self.server_name = data.get("server_name", "")
        try:
            self.server_id = int(data.get("server_id")) if data.get("server_id") not in (None, "") else None
        except (ValueError, TypeError):
            self.server_id = None
        self.channel_name = data.get("channel_name", "")
        try:
            self.channel_id = int(data.get("channel_id")) if data.get("channel_id") not in (None, "") else None
        except (ValueError, TypeError):
            self.channel_id = None
        self.random_sprites = bool(data.get("random_sprites", False))
        self.flagstring = data.get("flagstring", "")
        
        args = data.get("args_list")
        if isinstance(args, str):
            self.args_list = args.split()
        elif isinstance(args, list):
            self.args_list = args
        else:
            self.args_list = []
            
        self.hash = data.get("hash", "")
        self.seed = data.get("seed", "")

    @property
    def pk(self):
        return self.id

    def to_dict(self):
        ts_str = ""
        if isinstance(self.timestamp, datetime):
            ts_str = self.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        elif isinstance(self.timestamp, str):
            ts_str = self.timestamp
            
        return {
            'id': self.id,
            'creator_id': self.creator_id,
            'creator_name': self.creator_name,
            'seed_type': self.seed_type,
            'share_url': self.share_url,
            'timestamp': ts_str,
            'server_name': self.server_name,
            'server_id': self.server_id,
            'channel_name': self.channel_name,
            'channel_id': self.channel_id,
            'random_sprites': self.random_sprites,
            'flagstring': self.flagstring,
            'args_list': self.args_list,
            'hash': self.hash,
            'seed': self.seed
        }

    async def asave(self, update_fields=None):
        from bot.utils.firestore_client import db_async
        doc_ref = db_async.collection('seedlist').document(str(self.id))
        d = self.to_dict()
        if update_fields:
            update_data = {field: d.get(field) for field in update_fields if field in d}
            await doc_ref.update(update_data)
        else:
            await doc_ref.set(d)

    def save(self, update_fields=None):
        from bot.utils.firestore_client import db
        doc_ref = db.collection('seedlist').document(str(self.id))
        d = self.to_dict()
        if update_fields:
            update_data = {field: d.get(field) for field in update_fields if field in d}
            doc_ref.update(update_data)
        else:
            doc_ref.set(d)

class FirestoreSeedLogQuerySet:
    def __init__(self, docs):
        self.docs = docs

    def count(self):
        return len(self.docs)

    def order_by(self, field):
        reverse = field.startswith('-')
        clean_field = field.lstrip('-')
        
        def sort_key(doc):
            val = getattr(doc, clean_field, None)
            if val is None:
                if clean_field in ('id', 'creator_id', 'server_id', 'channel_id'):
                    return 0
                elif clean_field == 'timestamp':
                    return datetime.min.replace(tzinfo=timezone.utc)
                return ""
            if clean_field == 'timestamp':
                if isinstance(val, str):
                    parsed = parse_timestamp(val)
                    if isinstance(parsed, datetime):
                        return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=timezone.utc)
                    return datetime.min.replace(tzinfo=timezone.utc)
                elif isinstance(val, datetime):
                    return val if val.tzinfo is not None else val.replace(tzinfo=timezone.utc)
            return val

        sorted_docs = sorted(self.docs, key=sort_key, reverse=reverse)
        return FirestoreSeedLogQuerySet(sorted_docs)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.docs[item.start:item.stop:item.step]
        return self.docs[item]

    def values(self, *fields):
        if len(fields) == 1 and fields[0] == 'seed_type':
            return FirestoreSeedLogValuesQuerySet(self.docs, fields)
            
        results = []
        for doc in self.docs:
            d = doc.to_dict()
            row = {}
            for field in fields:
                row[field] = d.get(field)
            results.append(row)
        return results

class FirestoreSeedLogValuesQuerySet:
    def __init__(self, docs, fields):
        self.docs = docs
        self.fields = fields

    def annotate(self, **kwargs):
        from collections import Counter
        counter = Counter()
        for doc in self.docs:
            val = getattr(doc, 'seed_type', None)
            if val:
                counter[val] += 1
        
        results = []
        for seed_type, count in counter.items():
            results.append({
                'seed_type': seed_type,
                'roll_count': count
            })
        return FirestoreSeedLogAnnotatedQuerySet(results)

class FirestoreSeedLogAnnotatedQuerySet:
    def __init__(self, results):
        self.results = results

    def order_by(self, field):
        reverse = field.startswith('-')
        clean_field = field.lstrip('-')
        sorted_results = sorted(self.results, key=lambda x: x.get(clean_field, 0), reverse=reverse)
        return FirestoreSeedLogAnnotatedQuerySet(sorted_results)

    def first(self):
        if self.results:
            return self.results[0]
        return None

class SeedLogObjectsManager:
    def create(self, **kwargs):
        from bot.utils.firestore_client import db
        from google.cloud import firestore
        payload_template = self._prepare_payload(kwargs)
        
        counter_ref = db.collection('counters').document('seedlist')
        transaction = db.transaction()
        
        @firestore.transactional
        def create_entry_in_transaction(transaction, counter_ref, db, payload_template):
            snapshot = counter_ref.get(transaction=transaction)
            if snapshot.exists:
                current_id = snapshot.get("last_id")
            else:
                current_id = 0
            new_id = current_id + 1
            
            transaction.set(counter_ref, {"last_id": new_id})
            
            doc_ref = db.collection('seedlist').document(str(new_id))
            payload_data = {**payload_template, 'id': new_id}
            transaction.set(doc_ref, payload_data)
            
            return payload_data
            
        saved_payload = create_entry_in_transaction(transaction, counter_ref, db, payload_template)
        return FirestoreSeedLogAdapter(saved_payload)

    async def acreate(self, **kwargs):
        from bot.utils.firestore_client import db_async
        from google.cloud import firestore
        payload_template = self._prepare_payload(kwargs)
        
        counter_ref = db_async.collection('counters').document('seedlist')
        transaction = db_async.transaction()
        
        @firestore.async_transactional
        async def create_entry_in_transaction_async(transaction, counter_ref, db, payload_template):
            snapshot = await counter_ref.get(transaction=transaction)
            if snapshot.exists:
                current_id = snapshot.get("last_id")
            else:
                current_id = 0
            new_id = current_id + 1
            
            transaction.set(counter_ref, {"last_id": new_id})
            
            doc_ref = db.collection('seedlist').document(str(new_id))
            payload_data = {**payload_template, 'id': new_id}
            transaction.set(doc_ref, payload_data)
            
            return payload_data
            
        saved_payload = await create_entry_in_transaction_async(transaction, counter_ref, db_async, payload_template)
        return FirestoreSeedLogAdapter(saved_payload)

    def get(self, pk):
        from bot.utils.firestore_client import db
        doc = db.collection('seedlist').document(str(pk)).get()
        if not doc.exists:
            raise Exception(f"SeedLog with id {pk} not found")
        return FirestoreSeedLogAdapter(doc.to_dict(), doc_id=doc.id)

    async def aget(self, pk):
        from bot.utils.firestore_client import db_async
        doc = await db_async.collection('seedlist').document(str(pk)).get()
        if not doc.exists:
            raise Exception(f"SeedLog with id {pk} not found")
        return FirestoreSeedLogAdapter(doc.to_dict(), doc_id=doc.id)

    def filter(self, **kwargs):
        from bot.utils.firestore_client import db
        from google.cloud.firestore import FieldFilter
        query = db.collection('seedlist')
        for key, val in kwargs.items():
            if key == 'creator_id':
                query = query.where(filter=FieldFilter('creator_id', '==', int(val)))
            elif key == 'id__gt':
                query = query.where(filter=FieldFilter('id', '>', int(val)))
            elif key == 'seed_type':
                query = query.where(filter=FieldFilter('seed_type', '==', str(val)))
        
        docs = query.stream()
        adapters = [FirestoreSeedLogAdapter(doc.to_dict(), doc_id=doc.id) for doc in docs]
        return FirestoreSeedLogQuerySet(adapters)

    def _prepare_payload(self, kwargs):
        ts_val = kwargs.get('timestamp')
        ts_str = ""
        if isinstance(ts_val, datetime):
            ts_str = ts_val.strftime("%Y-%m-%dT%H:%M:%SZ")
        elif isinstance(ts_val, str):
            ts_str = ts_val
        else:
            ts_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        server_id = kwargs.get('server_id')
        if server_id not in (None, ""):
            try:
                server_id = int(server_id)
            except (ValueError, TypeError):
                server_id = None
        else:
            server_id = None

        channel_id = kwargs.get('channel_id')
        if channel_id not in (None, ""):
            try:
                channel_id = int(channel_id)
            except (ValueError, TypeError):
                channel_id = None
        else:
            channel_id = None

        creator_id = kwargs.get('creator_id') or 0
        try:
            creator_id = int(creator_id)
        except ValueError:
            creator_id = 0

        args_list = kwargs.get('args_list')
        if isinstance(args_list, str):
            args_list = args_list.split()
        elif args_list is None:
            args_list = []

        return {
            'creator_id': creator_id,
            'creator_name': str(kwargs.get('creator_name', 'anonymous')).strip(),
            'seed_type': str(kwargs.get('seed_type', 'ff6wc')).strip(),
            'share_url': str(kwargs.get('share_url', '')).strip() if kwargs.get('share_url') else None,
            'timestamp': ts_str,
            'server_name': str(kwargs.get('server_name', '')).strip() if kwargs.get('server_name') else None,
            'server_id': server_id,
            'channel_name': str(kwargs.get('channel_name', '')).strip() if kwargs.get('channel_name') else None,
            'channel_id': channel_id,
            'random_sprites': bool(kwargs.get('random_sprites', False)),
            'flagstring': str(kwargs.get('flagstring', '')).strip() if kwargs.get('flagstring') else None,
            'args_list': args_list,
            'hash': str(kwargs.get('hash', '')).strip() if kwargs.get('hash') else None,
            'seed': str(kwargs.get('seed', '')).strip() if kwargs.get('seed') else None
        }

class SeedLog:
    objects = SeedLogObjectsManager()
    DoesNotExist = Exception


class FeaturedPreset(models.Model):
    preset_name = models.CharField(max_length=255, primary_key=True)
    featured_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'featured_presets'

class UserFavorite(models.Model):
    user_id = models.BigIntegerField()
    preset_name = models.CharField(max_length=255, db_column='preset_name', default='')
    class Meta:
        db_table = 'user_favorites'
        unique_together = ('user_id', 'preset_name')

class APIKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='api_keys')
    key = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'api_keys'

    def __str__(self):
        return f"{self.user.username} - {self.name or 'Key'}"

@receiver(post_delete, sender=Preset)
def delete_featured_preset_on_preset_delete(sender, instance, **kwargs):
    try:
        FeaturedPreset.objects.filter(preset_name=instance.pk).delete()
    except Exception as e:
        print(f"Error during featured preset cleanup: {e}")

@receiver(post_save, sender=Preset)
def trigger_preset_validation(sender, instance, **kwargs):
    """
    When a Preset is saved, check if its validation is pending
    and launch the background task if so.
    """
    from .tasks import validate_preset_task

    if instance.validation_status == 'PENDING':
        validate_preset_task.delay(instance.pk)
