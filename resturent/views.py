from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from django.views.generic.base import View
from django.contrib.auth.models import User, auth
from resturent.models import UserProfile
import string
import random
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required



# Create your views here.
def token_generator(size=16, chars=string.ascii_uppercase + string.ascii_lowercase):
  return ''.join(random.choice(chars) for _ in range(size))

def refferal_code(size=5, chars=string.ascii_uppercase + string.ascii_lowercase):
  return ''.join(random.choice(chars) for _ in range(size))

def send_otp(size=4, chars=string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

class IndexView(View):

    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)

class AboutView(View):

    template_name = 'about.html'

    def get(self, request):
        return render(request, self.template_name)

class BookView(View):

    template_name = 'book.html'

    def get(self, request):
        return render(request, self.template_name)

class MenuView(View):

    template_name = 'menu.html'

    def get(self, request):
        return render(request, self.template_name)


class SigninView(View):

    template_name = 'signin.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect ('/profile')

        return render(request, self.template_name)
    def post(self, request):
        phoneno = request.POST.get('phoneno')
        password = request.POST.get('password')
        user = auth.authenticate(username=phoneno, password=password)
        if user is not None:
            # A backend authenticated the credentials
            auth.login(request, user)
            return redirect ('/profile')
        else:
            print('failed to login')
            messages.warning(request,"Invalid Creditional!!!!!!!!!!")
            return redirect ('/sign-in')
            # No backend authenticated the credentials


        return render(request, self.template_name)


class SignupView(View):

    template_name = 'signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect ('/profile')
        return render(request, self.template_name)
    def post(self, request):
        name = request.POST.get("name")
        phone_no = request.POST.get("phoneno")
        email = request.POST.get("email")
        refferal = request.POST.get("refferal")
        address = request.POST.get("address")
        pincode = request.POST.get("pincode")
        password = request.POST.get("password")
        otp = request.POST.get("otp")
        try:
            user = User.objects.filter(username=phone_no).first()
            if user:
                messages.warning(request,"Phone No already Exits!!!!!!!!!!")
                return redirect('/sign-up')
            if refferal:
                user = UserProfile.objects.filter(reffer_by=refferal).first()
                if user is None:
                    messages.warning(request,"Reffer code dose not exits!!!!!!!!!!")
                    return redirect('/sign-up')

            user = User.objects.create(username=phone_no,email=email)
            user.set_password(password)
            user.save()
        except Exception as e:
            print(e)
        try:
            userprofile = UserProfile.objects.create(user=user,name=name,phoneno=phone_no,reffer_by=refferal,address=address,pincode=pincode,refferal_code=refferal_code(),otp=send_otp(),is_active=True,token = token_generator(),dpimage='/profile/usericon.png')
            # print(userprofile.otp)
            # if userprofile.otp == otp:
            #     userprofile.is_active = True
            #     userprofile.token = token_generator()
            #     userprofile.save()
            messages.success(request,"You have registered successfully, now login!")
            return redirect('/sign-in')
        except Exception as e:
            print(e)
        
class SignUpajaxView(View):

    def post(self, request):
        phone_no = request.POST.get("phoneno")
        user = UserProfile.objects.filter(phoneno=phone_no).first()
        if user:
            print("Username is not unique")
        else:
            # UserValidate.objects.create(phoneno=phone_no,otp=otp())
            return HttpResponse("Html")
        # resturent JsonResponse({'data':"account sucessfully create"})

class AccountView(View):

    template_name = 'account.html'
    
    def get(self, request):
        # try:
        userprofile = request.user.userprofile
        print('user-dp',request.user.userprofile.dpimage)
        context = {'user':userprofile}
        if request.user.is_authenticated:
            return render(request, self.template_name, context)
        else:
            return redirect('/sign-in')
        # except :
        #     return redirect('/sign-in')

    def post(self,request):
        name = request.POST.get("name")
        address = request.POST.get("address")
        pincode = request.POST.get("pincode")
        about = request.POST.get("about")
        bio = request.POST.get("bio")
        phoneno = request.POST.get("phoneno")
        image = request.FILES.get("profilephoto")
        user = UserProfile.objects.get(phoneno=phoneno)
        if name:
            user.name = name
        if address:
            user.address = address
        if pincode:
            user.pincode = pincode
        if about:
            user.about = about
        if bio:
            user.bio = bio
        if image:
            user.dpimage = image
        user.save()

        messages.success(request,"Your Profile is Sucessfully Updated!")
        return redirect("/profile")
