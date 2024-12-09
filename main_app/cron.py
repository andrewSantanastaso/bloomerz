from .models import Plot

def update_date():
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
    return 'Days incremented'