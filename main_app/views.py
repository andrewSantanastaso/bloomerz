from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from .models import Garden, Plot, Plant
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import PlotForm
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
    return render(request, 'signup.html', context)



def home(request):
    return render(request, 'homepage.html')
    
def garden_index(request):
    gardens = Garden.objects.filter(user=request.user)
    plots = []
    for garden in gardens:
        plots.extend(garden.plot_set.all())
    return render(request, 'gardens/index.html', {'gardens': gardens, 'plots': plots})

def plant_index(request):
    garden = Garden.objects.filter(user=request.user)[:1].get()
    plots = Plot.objects.filter(garden=garden)
    plants = []
    for plot in plots:
        plants.extend(plot.plant_set.all())
    return render(request, 'plants/index.html', {'plants': plants})

def plot_index(request):
    user_gardens = Garden.objects.filter(user=request.user)
    plots = []
    for garden in user_gardens:
        plots.extend(garden.plot_set.all())
    
    return render(request, 'plots/index.html', { 'plots': plots})

class garden_detail(DetailView):
    model = Garden
    template_name = 'gardens/detail.html'

class GardenCreate(CreateView):
    model = Garden
    fields = ['name', 'location']
    template_name = 'gardens/create.html'
    # Assigns logged in user as the garden's owner
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GardenUpdate(UpdateView):
    model = Garden
    fields = ['name', 'location']
    template_name = 'gardens/update.html'

class GardenDelete(DeleteView):
    model = Garden
    template_name = 'gardens/delete.html'
    success_url = '/gardens/'



class CreatePlot(CreateView):
    model = Plot
    form_class = PlotForm

    template_name = 'plots/create.html'

    def form_valid(self, form):
        garden_id = self.kwargs['garden_id']
        garden = get_object_or_404(Garden, pk=garden_id)
        form.instance.garden = garden
      
            
        return super().form_valid(form)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        garden_id = self.kwargs.get('garden_id')  # Corrected this line
        context['garden'] = get_object_or_404(Garden, pk=garden_id)
        return context
    

def plot_detail(request, plot_id):
    plot = get_object_or_404(Plot, pk=plot_id)

    template_name = 'plots/detail.html'
    return render(request, template_name, {'plot': plot,'garden_id': plot.garden.id})
def water_plot(request, plot_id):
    plot = get_object_or_404(Plot, pk=plot_id)
    plot.dayssincewatered = 0
    plot.save()
    return redirect('garden-detail', pk=plot.garden.id)
    

class UpdatePlot(UpdateView):
    model = Plot
    fields = ['name', 'dayssincewatered']
    template_name = 'plots/update.html'

class DeletePlot(DeleteView):
    model = Plot
    success_url = '/gardens/'
    template_name = 'plots/plot_confirm_delete.html'

def plot_delete(request, plot_id):
    plot = get_object_or_404(Plot, pk=plot_id)
    plot.delete()
    return redirect('garden-detail', pk=plot.garden.id)


    
class CreatePlant(CreateView):
    model = Plant
    fields = ['name', 'dayssinceplanted', 'daysuntilmature', 'description']
    template_name = 'plants/create.html'
    # Assigns the plant with the first plot of the logged in user
    def form_valid(self, form):
        user_gardens = Garden.objects.filter(user=self.request.user)
        if user_gardens.exists():
            user_plots = Plot.objects.filter(garden=user_gardens.first())
            if user_plots.exists():
                form.instance.plot = user_plots.first()
        return super().form_valid(form)

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

class SignIn(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = '/gardens/'
