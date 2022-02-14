from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product, Store


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'oishi'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid credentials - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class ProductCreate(LoginRequiredMixin, CreateView):
  model = Product
  fields = ['name', 'category', 'description']

  def form_valid(self, form):
    # Assign the logged in user
    form.instance.user = self.request.user
    # Let the CreateView do its job as usual
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

@login_required
def products_index(request):
  products = Product.objects.filter(user = request.user)

  return render(request, 'products/index.html', { 'products': products })

@login_required
def products_detail(request, product_id):
  product = Product.objects.get(id=product_id)

  stores_product_doesnt_have = Store.objects.exclude(id__in = product.stores.all().values_list('id'))


  return render(request, 'products/detail.html', {

    'product': product, 

    'stores': stores_product_doesnt_have
  })


# @login_required
# def add_photo(request, product_id):
# 	# photo-file was the "name" attribute on the <input type="file">
#   photo_file = request.FILES.get('photo-file', None)
#   if photo_file:
#     s3 = boto3.client('s3')
#     # need a unique "key" for S3 / needs image file extension too
#     key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
#     # just in case something goes wrong
#     try:
#       s3.upload_fileobj(photo_file, BUCKET, key)
#       # build the full url string
#       url = f"{S3_BASE_URL}{BUCKET}/{key}"
    
#       photo = Photo(url=url, product_id=product_id)
#       photo.save()
#     except:
#       print('An error occurred uploading file to S3')
#   return redirect('detail', product_id=product_id)

@login_required
def assoc_store(request, product_id, store_id):
  Product.objects.get(id=product_id).stores.add(store_id)
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
  fields = '__all__'

class StoreUpdate(LoginRequiredMixin, UpdateView):
  model = Store
  fields = ['name', 'postcode','contact_infor']

class StoreDelete(LoginRequiredMixin, DeleteView):
  model = Store
  success_url = '/stores/'