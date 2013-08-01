from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Prints all project models and the count of objects in every model'

    def handle(self, *args, **options):
        models = ContentType.objects.all()
        for obj in models:
            self.stdout.write("%s - %d \n" % (obj.name, obj.model_class().objects.count(), ))
            self.stderr.write("error: %s - %d \n" % (obj.name, obj.model_class().objects.count(), ))