from django.core.management.base import BaseCommand
from main_app.models import Plot, Plant


class Command(BaseCommand):
    help = 'This is a test command'

    def handle(self, *args, **options):
        print('updating date')
        plots = Plot.objects.all()
        plants = Plant.objects.all()
        for plot in plots:
            plot.days_since_watered += 1
            plot.save()
        for plant in plants:
            plant.days_since_planted += 1
            plant.days_until_mature -= 1
            if plant.days_until_mature <= 0:
                plant.days_until_mature = 0
            plant.save()
