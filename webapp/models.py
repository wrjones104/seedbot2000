from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

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

class SeedLog(models.Model):
    id = models.AutoField(primary_key=True)
    creator_id = models.BigIntegerField()
    creator_name = models.TextField()
    seed_type = models.TextField()
    share_url = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    server_name = models.TextField(blank=True, null=True)
    server_id = models.BigIntegerField(blank=True, null=True)
    channel_name = models.TextField(blank=True, null=True)
    channel_id = models.BigIntegerField(blank=True, null=True)
    random_sprites = models.BooleanField(default=False)
    flagstring = models.TextField(null=True, blank=True)
    args_list = models.JSONField(default=list, null=True, blank=True)
    hash = models.TextField(blank=True, null=True)
    seed = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'seedlist'

class FeaturedPreset(models.Model):
    preset_name = models.CharField(max_length=255, primary_key=True)
    featured_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'featured_presets'

class UserFavorite(models.Model):
    user_id = models.BigIntegerField()
    preset = models.ForeignKey(Preset, on_delete=models.CASCADE, db_column='preset_name', to_field='preset_name')
    class Meta:
        db_table = 'user_favorites'
        unique_together = ('user_id', 'preset')

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
