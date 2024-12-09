from celery import shared_task
from main_app.models import Plot

@shared_task
def update_date():
    print('updating date')
    plots = Plot.objects.all()
    for plot in plots:
        
        plot.dayssincewatered += 1 

        plot.save()
    return 'Days incremented'