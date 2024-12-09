from django.core.management.base import BaseCommand
from main_app.models import Plot

class Command(BaseCommand):

    def handle(self, *args, **options):
        plots = Plot.objects.all()
        for plot in plots:
            plot.dayssincewatered += 1
            plot.save()
        
        return 'Days incremented'