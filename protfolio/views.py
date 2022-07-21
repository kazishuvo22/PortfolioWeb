from datetime import datetime
from django.contrib import messages, auth
from django.contrib.messages.storage import session
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse_lazy, reverse

from .forms import ContactForm
from .models import Contact, Skills, Education, WorkExperience
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout, authenticate, login


# Create your views here.
def index(request):
    page = 'home'
    return render(request, page + ".html")


def about(request):
    page = 'about'
    skills_all = []
    skills_all_category = Skills.objects.all().values_list('skills_category_name',
                                                           flat=True).distinct()
    for skills_cate in skills_all_category:
        skills = Skills.objects.filter(skills_category_name=skills_cate)
        skills_all.append({
            'category_name': skills_cate,
            'skills': skills,
            'skills_count': skills.count()
        })
    context = {
        'skills_all': skills_all
    }
    return render(request, page + ".html", context)


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


def logout_view(request):
    logout(request)
    messages.success(request, "Successfully Logout")
    return redirect('home')


def education(request):
    edu_all = Education.objects.all().order_by('-created_at')
    context = {
        'edu_all': edu_all
    }
    return render(request, "education.html", context)


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_staff:
                login(request, user)
                return HttpResponseRedirect(
                    reverse('admin:index'))
            else:
                return redirect('home')
        # Redirect to a success page.
        else:
            messages.warning(request, "Wrong Credentials! Please use correct username and password.")
    else:
        return render(request, "Login.html")


def workexperience(request):
    exp_all = WorkExperience.objects.all().order_by('-created_at')
    context = {
        'exp_all': exp_all
    }
    return render(request, "workexperience.html", context)
