from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_hello_world.hello.models import LogModelSignals
from django.contrib.contenttypes.models import ContentType


@receiver(post_save)
def on_create_or_save(sender, created, **kwargs):
    if ContentType.objects.get_for_model(sender) != ContentType.objects.get_for_model(LogModelSignals):
        LogModelSignals.objects.create(
            model=ContentType.objects.get_for_model(sender).model,
            event=(LogModelSignals.CREATION if created else LogModelSignals.EDITING),
        )


@receiver(post_delete)
def on_delete(sender, **kwargs):
    if ContentType.objects.get_for_model(sender) != ContentType.objects.get_for_model(LogModelSignals):
        LogModelSignals.objects.create(
            model=ContentType.objects.get_for_model(sender).model,
            event=LogModelSignals.DELETION,
        )