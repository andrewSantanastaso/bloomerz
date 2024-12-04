from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from .models import Garden, Plot, Plant
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('garden-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)



class Home(LoginView):
    template_name = 'home.html'
    
def garden_index(request):
    gardens = Garden.objects.all()
    for garden in gardens:
        plots = garden.plot_set.all()
    return render(request, 'gardens/index.html', {'gardens': gardens, 'plots': plots})

def plant_index(request):
    garden = Garden.objects.get(id=garden_id)
    plot = Plot.objects.get(id=plot_id)
    return render(request, 'plants/index.html', {'garden': garden, 'plot': plot})

class garden_detail(DetailView):
    model = Garden
    template_name = 'gardens/detail.html'

class GardenCreate(CreateView):
    model = Garden
    fields = '__all__'
    template_name = 'gardens/create.html'

class GardenUpdate(UpdateView):
    model = Garden
    fields = ['name', 'location']
    template_name = 'gardens/update.html'

class GardenDelete(DeleteView):
    model = Garden
    template_name = 'gardens/delete.html'
    success_url = '/gardens/'

class plot_index(ListView):
    model = Plot
    template_name = 'plots/index.html'

class CreatePlot(CreateView):
    model = Plot
    fields = '__all__'
    template_name = 'plots/create.html'

class PlotDetail(DetailView):
    model = Plot
    template_name = 'plots/detail.html'

class UpdatePlot(UpdateView):
    model = Plot
    fields = ['name', 'dayssincewatered']
    template_name = 'plots/update.html'

class DeletePlot(DeleteView):
    model = Plot
    template_name = 'plots/delete.html'
    success_url = '/gardens/'


    
class CreatePlant(CreateView):
    model = Plant
    fields = '__all__'
    template_name = 'plants/create.html'

class PlantDetail(DetailView):
    model = Plant
    template_name = 'plants/detail.html'

class UpdatePlant(UpdateView):
    model = Plant
    fields = ['name', 'dayssinceplanted', 'daysuntilmature', 'description']
    template_name = 'plants/update.html'

class DeletePlant(DeleteView):
    model = Plant
    template_name = 'plants/delete.html'
    success_url = '/gardens/'


