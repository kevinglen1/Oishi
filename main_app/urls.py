from django.urls import path,include
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('products/', views.products_index, name='index'),
  path('products/', views.products_index, name='index'),
  path('products/<int:product_id>/', views.products_detail, name='detail'),
  path('products/search_products/', views.search_products, name='search_products'),
  path('products/create/', views.ProductCreate.as_view(), name='products_create'),
  path('products/<int:pk>/update/', views.ProductUpdate.as_view(), name='products_update'),
  path('products/<int:pk>/delete/', views.ProductDelete.as_view(), name='products_delete'),
  path('products/<int:product_id>/assoc_store/<int:store_id>/', views.assoc_store, name='assoc_store'),
  path('products/<int:product_id>/unassoc_store/<int:store_id>/', views.unassoc_store, name='unassoc_store'),
#   path('products/<int:product_id>/add_photo/', views.add_photo, name='add_photo'),
  path('stores/', views.StoreList.as_view(), name='stores_index'),
  path('stores/<int:pk>/', views.StoreDetail.as_view(), name='stores_detail'),
  path('stores/create/', views.StoreCreate.as_view(), name='stores_create'),
  path('stores/<int:pk>/update/', views.StoreUpdate.as_view(), name='stores_update'),
  path('stores/<int:pk>/delete/', views.StoreDelete.as_view(), name='stores_delete'),
  path('accounts/', include('django.contrib.auth.urls')),
  path('accounts/signup', views.signup, name='signup'),
]