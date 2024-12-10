from .models import Plot

def urgent_plots_count(request):
    if request.user.is_authenticated:
        plots = Plot.objects.filter(garden__user=request.user)
        urgent_plots = [plot for plot in plots if plot.days_since_watered >= plot.frequency]
        return {'urgent_plots_count': len(urgent_plots)}
    return {'urgent_plots_count': 0}