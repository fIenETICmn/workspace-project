from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import User, Workspace, WorkspaceMemberInvite, WorkspaceMember
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import authenticate



@csrf_protect
def user_signup(request):
    if request.method == "POST":
        incoming_data = request.POST.dict()
        email = incoming_data["email"]
        password = incoming_data["password"]
        user = User.objects.create_user(
            password=password, email=email, create_workspace=True
        )

        return redirect("http://127.0.0.1:8000/login/")
    return render(request, "signup.html", {})


@csrf_protect
def user_login(request):
    if request.method == "POST":
        incoming_data = request.POST.dict()
        email = incoming_data["email"]
        password = incoming_data["password"]
        user = authenticate(email=email, password=password)
        print(user)

        if user.is_authenticated:
            if user.is_active:
                login(request, user)
                print("user logged in")
                return redirect('http://127.0.0.1:8000/homepage/')

        else:
            return redirect('http://127.0.0.1:8000/signup/')
    else:
        return render(request, "login.html", {})


def homepage(request):
    user = request.user
    print(user)


    return render(request, "homepage.html", {})

@csrf_protect
def worskpace_member_invite(request):
    user=request.user
    workspace = Workspace.objects.get(user=user)

    if request.method=="POST":
        incoming_data=request.POST.dict()


        subject = "Invitation"
        html_message = render_to_string("workspaceinvitation.html", {})
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ["kaushal@codefront.io"]
        send_mail(subject, "", email_from, recipient_list, html_message=html_message)

        workspacememberinvite=WorkspaceMemberInvite.objects.create(workspace=workspace, invited_by=user, invitee=recipient_list,accepted=True)
        workspacememberinvite.save()
        print(workspacememberinvite)

    return HttpResponse("send successfully")