from django.core.management.base import BaseCommand
from main_app.models import Plot, Plant


class Command(BaseCommand):
    help = 'This is a test command'

    def handle(self, *args, **options):
        print('updating date')
        plots = Plot.objects.all()
        plants = Plant.objects.all()
        for plot in plots:
            plot.dayssincewatered += 1
            plot.save()
        for plant in plants:
            plant.dayssinceplanted += 1
            plant.daysuntilmature -= 1
            if plant.daysuntilmature <= 0:
                plant.daysuntilmature = 0
            plant.save()
