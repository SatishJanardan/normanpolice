from django.shortcuts import render

# Blog functions
def home(request):
   return render(request, 'dashboard/home.html', context)

def about(request):
   return render(request, 'dashboard/about.html', {'title': 'About'})

