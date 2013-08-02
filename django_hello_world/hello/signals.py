from django.db.models.signals import post_save, post_delete
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from models import LogModelSignals


@receiver(post_save)
def on_create_or_save(sender, **kwargs):
    if (not kwargs.get('raw', False) and
            ContentType.objects.get_for_model(sender) != ContentType.objects.get_for_model(LogModelSignals)):
        LogModelSignals.objects.create(
            model=ContentType.objects.get_for_model(sender).model,
            event=(LogModelSignals.CREATION if kwargs.get('created', False) else LogModelSignals.EDITING),
        )


@receiver(post_delete)
def on_delete(sender, **kwargs):
    if ContentType.objects.get_for_model(sender) != ContentType.objects.get_for_model(LogModelSignals):
        LogModelSignals.objects.create(
            model=ContentType.objects.get_for_model(sender).model,
            event=LogModelSignals.DELETION,
        )