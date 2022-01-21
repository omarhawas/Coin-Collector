from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Coin, Addon
from .forms import OfferForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class CoinCreate(LoginRequiredMixin, CreateView):
  model = Coin
  fields = ['name', 'condition', 'description', 'age']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class CoinUpdate(LoginRequiredMixin, UpdateView):
  model = Coin
  fields = ['condition', 'description', 'age']

class CoinDelete(LoginRequiredMixin, DeleteView):
  model = Coin
  success_url = '/coins/'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def coins_index(request):
  coins = Coin.objects.filter(user=request.user)
  return render(request, 'coins/index.html', { 'coins': coins })

@login_required
def coins_detail(request, coin_id):
  coin = Coin.objects.get(id=coin_id)
  # Get the addons the coin doesn't have
  addons_coin_doesnt_have = Addon.objects.exclude(id__in = coin.addons.all().values_list('id'))
  # Instantiate OfferForm to be rendered in the template
  offer_form = OfferForm()
  return render(request, 'coins/detail.html', {
    # Pass the coin and offer_form as context
    'coin': coin, 'offer_form': offer_form,
    # Add the addons to be displayed
    'addons': addons_coin_doesnt_have
  })

@login_required
def add_offer(request, coin_id):
	# create the ModelForm using the data in request.POST
  form = OfferForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the coin_id assigned
    new_offer = form.save(commit=False)
    new_offer.coin_id = coin_id
    new_offer.save()
  return redirect('detail', coin_id=coin_id)


@login_required
def assoc_addon(request, coin_id, addon_id):
  Coin.objects.get(id=addon_id).addons.add(addon_id)
  return redirect('detail', coin_id=coin_id)

@login_required
def unassoc_addon(request, coin_id, addon_id):
  Coin.objects.get(id=coin_id).addons.remove(addon_id)
  return redirect('detail', coin_id=coin_id)

class AddonList(LoginRequiredMixin, ListView):
  model = Addon

class AddonDetail(LoginRequiredMixin, DetailView):
  model = Addon

class AddonCreate(LoginRequiredMixin, CreateView):
  model = Addon
  fields = '__all__'

class AddonUpdate(LoginRequiredMixin, UpdateView):
  model = Addon
  fields = ['name', 'color']

class AddonDelete(LoginRequiredMixin, DeleteView):
  model = Addon
  success_url = '/addons/'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'

  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)