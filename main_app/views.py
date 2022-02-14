from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Define the home view
def home(request):
  return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')

# class ProductCreate(CreateView):
#   model = Product
#   fields = ['_name', '_category', '_description', '_stores', '_postedby', '_avatar']
  
#   # This inherited method is called when a
#   # valid cat form is being submitted
#   def form_valid(self, form):
#     # Assign the logged in user (self.request.user)
#     form.instance.user = self.request.user  # form.instance is the cat
#     # Let the CreateView do its job as usual
#     return super().form_valid(form)

# def signup(request):
#   error_message = ''
#   if request.method == 'POST':
#     # This is how to create a 'user' form object
#     # that includes the data from the browser
#     form = UserCreationForm(request.POST)
#     if form.is_valid():
#       # This will add the user to the database
#       user = form.save()
#       # This is how we log a user in via code
#       login(request, user)
#       return redirect('index')
#     else:
#       error_message = 'Invalid sign up - try again'
#   # A bad POST or a GET request, so render signup.html with an empty form
#   form = UserCreationForm()
#   context = {'form': form, 'error_message': error_message}
#   return render(request, 'registration/signup.html', context)