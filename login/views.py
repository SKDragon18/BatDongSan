from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .forms import LoginForm, SignUpForm
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from .models import Nguoidung, Phanquyen
from random import choice
from string import digits
# Create your views here.

def sendMail(email,tieude,noidung):
    try:
        send_mail(tieude,
        noidung,
        'settings.EMAIL_HOST_USER',
        [email],
        fail_silently=False
        )
        return 1
    except:
        return 0

def random_id(length):
    return ''.join(choice(digits) for i in range(length))

class login(View):
    def get(self,request):
        info = LoginForm()
        return render(request,'accounts/login.html',{'form':info})

    def post(self,request):
        info = LoginForm(request.POST)
        if info.is_valid():
            username = info.cleaned_data['username']
            password = info.cleaned_data['password']
            print(password)
        try:
            myUser = User.objects.get(username = username)
            if myUser.check_password(password)or myUser.password == password:
                return render(request,'home/dashboard.html')
            else:
                error_password = "Mật khẩu không hợp lệ"
                return render(request,'accounts/login.html',{'form':info,'error_password':error_password})
        except:
                error_username = "Tài khoản không tồn tại"
                return render(request,'accounts/login.html',{'form':info,'error_username':error_username})
               
class createAccount(View):
    def get(self,request):
        signUp = SignUpForm()
        return render(request, 'accounts/register.html',{'form':signUp})

    def post(self,request):
        signUp = SignUpForm(request.POST)
        if not signUp.is_valid():
            return render(request,'accounts/register.html',{'form':signUp})
        else:
            username = signUp.cleaned_data['username']
            password = signUp.cleaned_data['password1']
            email = signUp.cleaned_data['email']
            ho = signUp.cleaned_data['ho']
            ten=signUp.cleaned_data['ten']
            gioitinh=signUp.cleaned_data['gioitinh']
            sdt=signUp.cleaned_data['sdt']
            randomCode = random_id(6)
            # sendMail(email,"EXAM CODE",randomCode)
            print("code moi tao:" + randomCode)
            request.session['randomCode'] = randomCode
            request.session['user'] = {'username':username,'password':password,'email':email,'ho':ho,'ten':ten,'gioitinh':gioitinh,'sdt':sdt}
            return render(request,'accounts/checkCode.html')

class checkCode(View):
    def post(self, request):
        code = request.POST['code']
        randomCode = request.session['randomCode']
        user = request.session['user']
        print("codenhan" + code)
        print("codegui" + randomCode)
        if code == randomCode:
            myUser = User()
            nguoidung = Nguoidung()
            myUser.username = user['username']
            myUser.password = user['password']
            myUser.email = user['email']
            nguoidung.tendangnhap = user['username']
            nguoidung.ho=user['ho']
            nguoidung.ten=user['ten']
            nguoidung.gioitinh=user['gioitinh']
            nguoidung.sdt=user['sdt']
            nguoidung.matkhau = user['password']
            nguoidung.email = user['email']
            nguoidung.phanquyen = Phanquyen.objects.get(maquyen='USER')
            nguoidung.khoa = 0
            try:
                nguoidung.save()
                myUser.save()
                myUser.groups.add(Group.objects.get(name='user'))
                myUser.save()
                info = LoginForm()
                return render(request,'accounts/login.html',{'success_created_user': "Tạo tài khoản thành công!", 'form':info})
            except:
                print("luu nguoi dung khong duoc")
                print(myUser.username)            
                info = LoginForm()
                return render(request,'accounts/login.html',{'error_created_user': "Tạo tài khoản thất bại, vui lòng thử lại sau!",'form':info})
        else:
            error_code = "Mã không hợp lệ, vui lòng nhập lại"
            return render(request,'accounts/checkCode.html',{'error_code': error_code})

def info(request):
    return render(request, 'home/information.html')

class forgot(View):
    def get(self,request):
        return render(request,'accounts/forgot.html')
    
    def post(self,request):
        username=request.POST['username']
        email = request.POST['email']
        try:
            user = User.objects.get(username=username)
            nguoidung = Nguoidung.objects.get(tendangnhap=username)
            print(username)
            if user.email == email:
                new_password = random_id(8)
                # sendMail(email=email,tieude="Mật khẩu sau khi được reset",noidung=new_password)
                print('mật khẩu mới: ',end='')
                print(new_password)
                try:
                    user.password = new_password
                    nguoidung.matkhau = new_password
                    user.save()
                    nguoidung.save()
                    info = LoginForm()
                    return render(request,'accounts/login.html',{'success_reset_password':"Mật khẩu đã được reset, vui lòng kiểm tra gmail",'form':info})
                except:
                    return HttpResponse("Lỗi, vui lòng thử lại sau")
            else:
                return render(request,'accounts/forgot.html',{'wrong_email':"Email không hợp lệ, vui lòng kiểm tra lại email"})
        except:
            return render(request,'accounts/forgot.html',{'wrong_username':"Tài khoản không tồn tại!"})
