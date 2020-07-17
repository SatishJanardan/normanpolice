from django.shortcuts import render

# Setup the hello world call
def hello_world(request):
    return render(request, 'hello_world.html', {})
