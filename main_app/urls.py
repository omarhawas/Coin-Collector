from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('coins/', views.coins_index, name='index'),
  path('coins/<int:coin_id>/', views.coins_detail, name='detail'),
  path('coins/create/', views.CoinCreate.as_view(), name='coins_create'),
  path('coins/<int:pk>/update/', views.CoinUpdate.as_view(), name='coins_update'),
  path('coins/<int:pk>/delete/', views.CoinDelete.as_view(), name='coins_delete'),
  path('coins/<int:coin_id>/add_offer/', views.add_offer, name='add_offer'),
  path('coins/<int:coin_id>/assoc_addon/<int:addon_id>/', views.assoc_addon, name='assoc_addon'),
  path('coins/<int:coin_id>/unassoc_addon/<int:addon_id>/', views.unassoc_addon, name='unassoc_addon'),
  path('addons/', views.AddonList.as_view(), name='addons_index'),
  path('addons/<int:pk>/', views.AddonDetail.as_view(), name='addons_detail'),
  path('addons/create/', views.AddonCreate.as_view(), name='addons_create'),
  path('addons/<int:pk>/update/', views.AddonUpdate.as_view(), name='addons_update'),
  path('addons/<int:pk>/delete/', views.AddonDelete.as_view(), name='addons_delete'),
  path('accounts/signup/', views.signup, name='signup'),
]