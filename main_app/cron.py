from .models import Plot

def update_date():
    print('updating date')
    plots = Plot.objects.all()
    for plot in plots:
        
        plot.days_since_watered += 1 

        plot.save()
    return 'Days incremented'