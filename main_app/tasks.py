from celery import shared_task
from .models import Plot
from django.utils import timezone


@shared_task
def increment_days_for_water():
    today = timezone.now().date()
    plots = Plot.objects.all()
    for plot in plots:
        if plot.last_watered != today:
            plot.dayssincewatered += 1 

        plot.save()
    return 'Days incremented'