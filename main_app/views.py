from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from .models import Garden, Plot, Plant
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import PlotForm, GardenForm, PlantForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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


def home(request):
    return render(request, 'homepage.html')

@login_required    
def garden_index(request):
    gardens = Garden.objects.filter(user=request.user)
    plots = []
    for garden in gardens:
        plots.extend(garden.plot_set.all())
    return render(request, 'gardens/index.html', {'gardens': gardens, 'plots': plots})

@login_required
def plant_index(request):
    garden = Garden.objects.filter(user=request.user)[:1].get()
    plots = Plot.objects.filter(garden=garden)
    plants = []
    for plot in plots:
        plants.extend(plot.plant_set.all())
    return render(request, 'plants/index.html', {'plants': plants})

@login_required
def plot_index(request):
    user_gardens = Garden.objects.filter(user=request.user)
    plots = []
    for garden in user_gardens:
        plots.extend(garden.plot_set.all())
    
    return render(request, 'plots/index.html', { 'plots': plots})

class garden_detail(LoginRequiredMixin,DetailView):
    model = Garden
    template_name = 'gardens/detail.html'

class GardenCreate(LoginRequiredMixin,CreateView):
    model = Garden
    fields = ['name', 'location']
    template_name = 'gardens/create.html'
    # Assigns logged in user as the garden's owner
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GardenUpdate(LoginRequiredMixin,UpdateView):
    model = Garden
    form_class = GardenForm
    template_name = 'gardens/update.html'

class GardenDelete(LoginRequiredMixin,DeleteView):
    model = Garden
    template_name = 'gardens/delete.html'
    success_url = '/gardens/'

class CreatePlot(LoginRequiredMixin,CreateView):
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
        garden_id = self.kwargs.get('garden_id')
        context['garden'] = get_object_or_404(Garden, pk=garden_id)
        return context
    

@login_required
def plot_detail(request, plot_id):
    plot = get_object_or_404(Plot, pk=plot_id)
    
    show_form = request.GET.get('add_plant') == 'true'
    
    if request.method == 'POST':
        form = PlantForm(request.POST)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.plot = plot
            plant.save()
            return redirect('plot-detail', plot_id=plot.id)
    else:
        form = PlantForm() if show_form else None

    template_name = 'plots/detail.html'
    return render(request, template_name, {'plot': plot, 'form': form, 'garden_id': plot.garden.id, 'show_form': show_form})

@login_required
def water_plot(request, plot_id):
    plot = get_object_or_404(Plot, pk=plot_id)
    plot.days_since_watered = 0
    plot.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required
def urgent_plots(request):
    user_gardens = Garden.objects.filter(user=request.user)
    urgent_plots = []
    for garden in user_gardens:
        plots = garden.plot_set.all()
        
    
    
        for plot in plots:
            
            if plot.days_since_watered >= plot.frequency:
                urgent_plots.append(plot)
    if len(urgent_plots) == 0:
        return render(request, 'gardens/index.html', {'gardens': user_gardens})
    return render(request, 'plots/urgent.html', {'urgent_plots': urgent_plots})


class UpdatePlot(LoginRequiredMixin,UpdateView):
    model = Plot
    fields = ['name', 'days_since_watered', 'frequency']
    template_name = 'plots/update.html'

class DeletePlot(LoginRequiredMixin,DeleteView):
    model = Plot
    success_url = '/gardens/'
    template_name = 'plots/plot_confirm_delete.html'

@login_required
def plot_delete(request, plot_id):
    plot = get_object_or_404(Plot, pk=plot_id)
    plot.delete()
    return redirect('garden-detail', pk=plot.garden.id)
    
class CreatePlant(LoginRequiredMixin,CreateView):
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

class PlantDetail(LoginRequiredMixin,DetailView):
    model = Plant
    template_name = 'plants/detail.html'

class UpdatePlant(LoginRequiredMixin,UpdateView):
    model = Plant
    form_class git = PlantForm
    template_name = 'plants/update.html'

class DeletePlant(LoginRequiredMixin,DeleteView):
    model = Plant
    template_name = 'plants/delete.html'

class SignIn(LoginRequiredMixin,LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    success_url = '/gardens/'