from django.shortcuts import render, redirect
from django.views import generic
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
import json, re
from django.contrib.auth import login, logout, authenticate


class RegisterView(generic.View):
    model = User
    template_name = 'Register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            try :
                data = json.loads(request.body)
                username = data.get('Username')
                if User.objects.filter(username=username).exists():
                    return JsonResponse({"message": "Username already exists"}, status=400)
                email = data.get('Email')
                if User.objects.filter(email=email).exists():
                    return JsonResponse({"message": "Email already exists"}, status=400)
                FirstName = data.get('FirstName')
                LastName = data.get('LastName')
                password = data.get('password')
                User_group = Group.objects.get(name='Customer')
                user = User(username=username,email=email,first_name=FirstName, last_name = LastName)
                user.set_password(password)
                user.save()
                user.groups.add(User_group)
                return redirect('login')
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        else :
            return render(request, self.template_name)

class LoginView(generic.View):
    success_url = '/'
    template_name = "login.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            try :
                data = json.loads(request.body)
                username = data.get('Username')
                password = data.get('Password')
                getUser = User.objects.filter(email=username).first()
                if not getUser :
                    getUser = User.objects.get(username=username)
                    user = authenticate(username=username, password=password)
                    if user :
                        login(request,user)
                        return JsonResponse({"redirect_url": self.success_url, "message" : "Logged in successfully !! "})
                else: 
                    user = authenticate(username=getUser.username, password=password)
                    if user :
                        login(request,user)
                        return JsonResponse({"redirect_url": self.success_url, "message" : "Logged in successfully !! "})

            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        else :
            return render(request, self.template_name)

class LogoutView(generic.View):
    success_url = "accounts/login/"

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.success_url)  

