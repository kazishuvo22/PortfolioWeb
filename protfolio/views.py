from django.shortcuts import render , HttpResponseRedirect, redirect
from .forms import ContactForm
from .models import Contact

# Create your views here.
def index(request):
    page = 'home'
    return render(request, page+".html")

def about(request):
    page = 'about'
    return render(request, page+".html")

def resume(request):
    page = 'resume'
    return render(request, page+".html")

def contact(request):
    page = 'contact'
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = request.POST['name']
            email = request.POST['email']
            subject = request.POST['subject']
            message = request.POST['message']
            create_msg = Contact.objects.create(name= name, email=email, subject=subject, message = message)
            return redirect('contact')

    else:
        form = ContactForm()
    return render(request, page+".html", {'form': form})