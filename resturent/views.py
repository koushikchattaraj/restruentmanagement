from django import http
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from django.views.generic.base import View
from django.contrib.auth.models import AnonymousUser, User, auth
from resturent.models import Feed, UserProfile
import string
import random
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import sys
from  PIL  import Image
from django.core.files.storage import FileSystemStorage





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
        if request.user.is_authenticated:
            playerlist = UserProfile.objects.filter(role="player").exclude(user=request.user)
        else:
            playerlist = UserProfile.objects.filter(role="player")
        context = {
            'playerlist':playerlist
        }
        return render(request, self.template_name,context)

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
        if request.user.is_authenticated:
            playerlist = UserProfile.objects.filter(role="player").exclude(user=request.user)
        else:
            playerlist = UserProfile.objects.filter(role="player")
        context = {
            'playerlist':playerlist
        }
        return render(request, self.template_name,context)


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
        playingtype = request.POST.get("type")
        address = request.POST.get("address")
        pincode = request.POST.get("pincode")
        password = request.POST.get("password")
        otp = request.POST.get("otp")
        try:
            user = User.objects.filter(username=phone_no).first()
            if user:
                messages.warning(request,"Phone No already Exits!!!!!!!!!!")
                return redirect('/sign-up')

            user = User.objects.create(username=phone_no,email=email)
            user.set_password(password)
            user.save()
        except Exception as e:
            messages.warning(request,e)
            return redirect('/sign-up')

        try:
            userprofile = UserProfile.objects.create(user=user,name=name,phoneno=phone_no,email=email,address=address,pincode=pincode,otp=send_otp(),is_active=True,token = token_generator(),dpimage='/profile/usericon.png',role='player',type=playingtype)
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
        
        try:
            if request.user.is_authenticated:
                userprofile = request.user.userprofile
                newsfeed = Feed.objects.filter(user=request.user)
                context = {
                    'userprofile':userprofile,
                    'newsfeed':newsfeed
                    }
                return render(request, self.template_name, context)
            else:
                return redirect('/sign-in')
        except Exception as e:
            return redirect('/')

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
            # folder = "media/profile"
            # fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT  
            # filename = fs.save(image.name, image)
            # file_url = fs.url(filename)
            # print("*********")
            # img = cv.imread(f"media/profile/{image.name}", cv.IMREAD_UNCHANGED)
            # original = img.copy()

            # l = int(max(5, 6))
            # u = int(min(6, 6))

            # ed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            # edges = cv.GaussianBlur(img, (21, 51), 3)
            # edges = cv.cvtColor(edges, cv.COLOR_BGR2GRAY)
            # edges = cv.Canny(edges, l, u)

            # _, thresh = cv.threshold(edges, 0, 255, cv.THRESH_BINARY  + cv.THRESH_OTSU)
            # kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
            # mask = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=4)

            # data = mask.tolist()
            # sys.setrecursionlimit(10**8)
            # for i in  range(len(data)):
            #     for j in  range(len(data[i])):
            #         if data[i][j] !=  255:
            #             data[i][j] =  -1
            #         else:
            #             break
            #     for j in  range(len(data[i])-1, -1, -1):
            #         if data[i][j] !=  255:
            #             data[i][j] =  -1
            #         else:
            #             break
            # image = np.array(data)
            # image[image !=  -1] =  255
            # image[image ==  -1] =  0

            # mask = np.array(image, np.uint8)

            # result = cv.bitwise_and(original, original, mask=mask)
            # result[mask ==  0] =  255
            # cv.imwrite('bg.png', result)

            # img = Image.open('bg.png')
            # img.convert("RGBA")
            # datas = img.getdata()

            # newData = []
            # for item in datas:
            #     if item[0] ==  255  and item[1] ==  255  and item[2] ==  255:
            #         newData.append((255, 255, 255, 0))
            #     else:
            #         newData.append(item)

            # img.putdata(newData)
            # img.save("media/profile/img.png", "PNG")

            user.dpimage = image

        user.save()
        

        messages.success(request,"Your Profile is Sucessfully Updated!")
        return redirect("/profile")

class PostFeedView(View):

    def post(self,request):
        user = User.objects.get(username=request.user)
        feed = Feed.objects.create(user=user)
        postimage = request.FILES.get("postimage")
        title = request.POST.get("title")
        des = request.POST.get("des")
        if postimage:
            feed.postimage = postimage
        if title:
            feed.title = title
        if des:
            feed.descrption = des
        feed.save()
        messages.success(request,"Post Created!")
        return redirect("/profile")

class AllUserView(View):

    template_name = 'profilelist.html'

    def get(self, request):
        if request.user.is_authenticated:
            userlist = UserProfile.objects.filter(role="user").exclude(user=request.user)
        else:
            userlist = UserProfile.objects.filter(role="user")

        context = {
            'userlist':userlist
        }
        return render(request, self.template_name, context)

class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect ("/")

class ProfileView(View):
    template_name = 'profile.html'


    def get(self,request,pk):
        userprofile = UserProfile.objects.get(id=pk)
        user = User.objects.get(username = userprofile.phoneno )
        feed = Feed.objects.filter(user=user)
        userobj = UserProfile.objects.filter(id=pk).first()
        context = {
            'userobj':userobj,
            'feedobj':feed
        }
        return render(request, self.template_name, context)


