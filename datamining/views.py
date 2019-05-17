from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def something(request):
    print('Something happened')
    print('Something happened')
    print('Something happened')
    print('Something happened')
    print('Something happened')
    print('Something happened')
    print('Something happened')
    print('Something happened')
    return render(request, 'index.html')