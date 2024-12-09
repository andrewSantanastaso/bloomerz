from django.core.management.base import BaseCommand
from main_app.models import Plot


class Command(BaseCommand):
    help = 'This is a test command'

    def handle(self, *args, **options):
        print('updating date')
        plots = Plot.objects.all()
        for plot in plots:
            plot.dayssincewatered += 1
            plot.save()
