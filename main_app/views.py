from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'gaoishi'
import uuid
import boto3
from .models import Product, Store, Photo


S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'gaoishi'

def search_products(request):
  if request.method == "POST":
    searched = request.POST['searched']
    products = Product.objects.filter(name__contains=searched)

    return render(request, 'products/search_products.html', {'searched': searched, 'products': products})
  else:
    return render(request, 'products/search_products.html', {})



def signup(request):
  error_message = ''
  if request.method == 'POST':
    
    form = UserCreationForm(request.POST)
    if form.is_valid():
     
      user = form.save()
      
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid credentials - try again'
 
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class ProductCreate(LoginRequiredMixin, CreateView):
  model = Product
  fields = ['name', 'category', 'description']

  def form_valid(self, form):
   
    form.instance.user = self.request.user
    
    return super().form_valid(form)

class ProductUpdate(LoginRequiredMixin, UpdateView):
  model = Product
  fields = ['name', 'category', 'description']

class ProductDelete(LoginRequiredMixin, DeleteView):
  model = Product
  success_url = '/products/' 

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')


def products_index(request):
  products = Product.objects.all()

  return render(request, 'products/index.html', { 'products': products })

def products_detail(request, product_id):
  product = Product.objects.get(id=product_id)

  stores_product_doesnt_have = Store.objects.exclude(id__in = product.stores.all().values_list('id'))


  return render(request, 'products/detail.html', {

    'product': product, 

    'stores': stores_product_doesnt_have
  })


@login_required
def add_photo(request, product_id):
	
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
   
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
    
      photo = Photo(url=url, product_id=product_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('detail', product_id=product_id)

@login_required
def assoc_store(request, product_id):
  if request.method == "POST":
    ab = request.POST['store']
    print(ab)
  Product.objects.get(id=product_id).stores.add(ab)
  return redirect('detail', product_id=product_id)

@login_required
def unassoc_store(request, product_id, store_id):
  Product.objects.get(id=product_id).stores.remove(store_id)
  return redirect('detail', product_id=product_id)

class StoreList(LoginRequiredMixin, ListView):
  model = Store

class StoreDetail(LoginRequiredMixin, DetailView):
  model = Store

class StoreCreate(LoginRequiredMixin, CreateView):
  model = Store
  fields = ['name','postcode','contact_infor']
  success_url = '/stores/'

class StoreUpdate(LoginRequiredMixin, UpdateView):
  model = Store
  fields = ['name', 'postcode','contact_infor']
  success_url = '/stores/'

class StoreDelete(LoginRequiredMixin, DeleteView):
  model = Store
  success_url = '/stores/'