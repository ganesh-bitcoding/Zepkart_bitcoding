from django.shortcuts import render, redirect
from django.views import generic
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
import json, re
from django.contrib.auth import login, logout, authenticate
from .models import Seller
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(generic.View):
    model = User
    template_name = 'Authentication/Register.html'

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
    template_name = "Authentication/login.html"
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

class BeSellerView(LoginRequiredMixin, generic.View):
    model=Seller
    template_name="Authentication/beSeller.html"
    def get(self, request, *args, **kwargs):
        context = {
            "title": "Be Seller" 
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            try :
                if request.content_type == "application/json":
                    data = json.loads(request.body.decode("utf-8"))
                else:
                    data = request.POST

                store_name = data.get('store_name')  # fixed key
                phone_number = data.get('phone_number')
                address = data.get('address')
                business_type = data.get('business_type')
                gst_number = data.get('gst_number')
                pan_number = data.get('pan_number')
                bank_account_number = data.get('bank_account_number')
                ifsc_code = data.get('ifsc_code')
                bank_name = data.get('bank_name')
                pickup_address = data.get('pickup_address')
                return_address = data.get('return_address')
                User_group = Group.objects.get(name='Seller')
                user = request.user
                new_seller = Seller.objects.create(
                user=user,
                store_name=store_name,
                phone_number=phone_number,
                address=address,
                business_type=business_type,
                gst_number=gst_number,
                pan_number=pan_number,
                bank_account_number=bank_account_number,
                ifsc_code=ifsc_code,
                bank_name=bank_name,
                pickup_address=pickup_address,
                return_address=return_address,
            )
                user.groups.add(User_group)
                print(user.groups.get())
                
                return redirect('login')
            except Exception as e:
                return render(request, self.template_name)
        else :
            return render(request, self.template_name)
    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = "Be Seller"
        return context