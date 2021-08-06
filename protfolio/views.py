from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import ContactForm
from .models import Contact
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
def index(request):
    page = 'home'
    return render(request, page + ".html")


def about(request):
    page = 'about'
    return render(request, page + ".html")


def resume(request):
    page = 'resume'
    return render(request, page + ".html")


def contact(request):
    page = 'contact'
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            now = datetime.now()
            name = request.POST['name']
            email = request.POST['email']
            subject = request.POST['subject']
            message = request.POST['message']
            create_msg = Contact.objects.create(name=name, email=email, subject=subject, message=message, ctime=now)
            messages.success(request, "Your message is submitted successfully!!!")
            return redirect('contact')

    else:
        form = ContactForm()
    return render(request, page + ".html", {'form': form})


@staff_member_required
def control_panel(request):
    page = 'control_panel'

    return render(request, page + ".html")


@staff_member_required
def messages_list(request):
    page = 'messages'
    context = {
        'message_all': Contact.objects.all()
    }
    return render(request, page + ".html", context)


@staff_member_required
def delete_messages(request, mid):
    msg = Contact.objects.get(id=mid)
    msg.delete()
    return redirect('message_list')
