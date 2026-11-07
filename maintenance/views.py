from django.shortcuts import render,redirect
from .models import Test
from .forms import TestForm

# Create your views here.


def test(request):
    tests = Test.objects.all()
    context = {'tests': tests}
    return render(request,'maintenance/test.html',context)

def createTest(request):
    form = TestForm()
    
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("test")
    

    context = {'form': form}
    return render(request, 'maintenance/modification_form.html', context)






def index (request):
    return render(request,'base.html')


def logoutUser(request):
    logout(request)
    return redirect('login')