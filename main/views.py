from django.shortcuts import render
from django.http import HttpResponse
from .models import Baidang, Phanquyen, Nguoidung, Hinhanh, DsYeuthich, Nha,Chungcu
from django.views import View
from django.db import connection
from .forms import BaiDangForm, NhaForm, ChungCuForm
from .models import UploadedFile
from unidecode import unidecode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def index(request):
    return render(request, template_name='main/index.html')

def home(request):
    return render(request, template_name='main/home.html')


def tao_id_baidang():
    try:
        with connection.cursor() as cursor:
            cursor.execute('Select dbo.SinhIdBaiDang()')
            result=cursor.fetchone()[0]
            cursor.close()
    except Exception as e:
        return e
    return result

def tao_id_hinhanh():
    try:
        with connection.cursor() as cursor:
            cursor.execute('Select dbo.SinhIdHinhAnh()')
            result=cursor.fetchone()[0]
            cursor.close()
    except Exception as e:
        return e
    return result




class DangTin(View):

    def get(self,request,loai):
        f=BaiDangForm(prefix='f')
        if loai =='Nha':
            fh=NhaForm(prefix='fh')
        else:
            fh=ChungCuForm(prefix='fh')
        
        f.fields['id_baidang'].initial=int(tao_id_baidang())
        f.fields['loai'].initial=str.upper(loai)
        f.fields['chudang'].initial='cá nhân'
        f.fields['id_baidang'].widget.attrs['readonly'] = True
        f.fields['ngaydang'].widget.attrs['readonly'] = True
        return render(request,'main/forms_dang.html',{'f':f, 'fh':fh,'loai':loai})
    
    def post(self,request,loai):
        f=BaiDangForm(request.POST,prefix='f')
        if loai =='Nha':
            fh=NhaForm(request.POST,prefix='fh')
        else:
            fh=ChungCuForm(request.POST,prefix='fh')
        
        if f.is_valid() and fh.is_valid():
            file_list=list(request.FILES.getlist('files'))
            if len(file_list)<3:
                    return render(request,'main/forms_dang.html',{'f':f, 'fh':fh,'loai':loai,'message':'Mời chọn ít nhất 3 hình ảnh'})
            
            baidang = f.save(commit=False)
            user='admin'
            baidang.tendangnhap=Nguoidung.objects.get(pk=user)
            baidang.trangthai=0
            baidang.save()
            baidangnha = fh.save(commit=False)
            if loai=='Nha':
                baidangnha.manha = baidang
            else:
                baidangnha.machungcu=baidang
            baidangnha.save()
            try:
                
                
                for uploaded_file in file_list:
                    file=UploadedFile.objects.create(file=uploaded_file)
                    hinh_anh=Hinhanh()
                    hinh_anh.id_hinhanh=tao_id_hinhanh()
                    hinh_anh.nguon=file.file.url
                    hinh_anh.id_baidang=baidang
                    hinh_anh.save() 
                    
                return render(request,'main/thanh_cong.html',{'message':'Thành công'})
                
            except Exception as e:
                return HttpResponse(e)
        else:
            print('Bài đăng')
            for error in f.errors:
                print(error)
            print('Nhà')
            for error in fh.errors:
                print(error)
            return render(request,'main/thanh_cong.html',{'message':'Thất bại'})

def tao_phan_trang(request,ds):
    paginator = Paginator(ds, 5)
    try:
        page= request.GET.get('page')
        ds=paginator.get_page(page)
    except PageNotAnInteger:
        ds=paginator.get_page(1)
    except EmptyPage:
        ds=paginator.get_page(paginator.num_pages)
    return ds

def ds_baidang_timkiem(user,timkiem=None):
    if timkiem is None:
        return Baidang.objects.raw("SELECT * FROM BAIDANG where tendangnhap='"+user+"' and trangthai = 1")
    else:
        if timkiem.isdigit():
            ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where tendangnhap = %s and trangthai = 1 and (id_baidang = %s "+
                                           "or ngaydang LIKE %s)",[user,timkiem,'%'+timkiem+'%'])
        else: 
            chuoi_chuan_hoa= str.upper(unidecode(timkiem))
            ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where tendangnhap= %s and trangthai = 1 and (tieude LIKE %s or loai LIKE %s)",[user,'%'+timkiem+'%','%'+chuoi_chuan_hoa+'%'])
        return ds_baidang

class DanhSachBaiDang(View):
    
    def get(self, request):
        user='admin'

        if request.GET.get('timkiem'):
            timkiem=request.GET.get('timkiem')
            ds_baidang=ds_baidang_timkiem(user,timkiem)  
        else:
            ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where tendangnhap='"+user+"' and trangthai = 1")
        ds_baidang=tao_phan_trang(request,ds_baidang)
        if request.GET.get('timkiem'):
            return render(request,'main/ds_baidang.html',{'ds':ds_baidang,'timkiem':request.GET.get('timkiem')})
        return render(request,'main/ds_baidang.html',{'ds':ds_baidang})

    def post(self,request):
        user='admin'
        
        if not request.POST["timkiem"]:
            ds_baidang=ds_baidang_timkiem(user=user)
            ds_baidang=tao_phan_trang(request,ds_baidang)
            return render(request,'main/ds_baidang.html',{'ds':ds_baidang})
        
        timkiem=request.POST["timkiem"]
        ds_baidang=ds_baidang_timkiem(user,timkiem)
        ds_baidang=tao_phan_trang(request,ds_baidang)
        return render(request,'main/ds_baidang.html',{'ds':ds_baidang,'timkiem':timkiem})

def ds_yeuthich_timkiem(user,timkiem=None):
    if timkiem is None:
        return Baidang.objects.raw("SELECT * FROM BAIDANG where id_baidang in (SELECT id_baidang FROM DS_YEUTHICH where tendangnhap='"+user+"') and trangthai=1")
    else:
        if timkiem.isdigit():
            ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where trangthai=1 and ((id_baidang in (SELECT id_baidang FROM DS_YEUTHICH where id_baidang = %s and tendangnhap= %s ))"
                                           + " or (id_baidang in (SELECT id_baidang FROM DS_YEUTHICH where tendangnhap= %s ) and ngaydang LIKE %s))",[timkiem,user,user,'%'+timkiem+'%'])
        else: 
            chuoi_chuan_hoa= str.upper(unidecode(timkiem))
            ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where id_baidang in (SELECT id_baidang FROM DS_YEUTHICH where tendangnhap= %s ) and trangthai = 1 and (tieude LIKE %s or loai LIKE %s)",[user,'%'+timkiem+'%','%'+chuoi_chuan_hoa+'%'])
        return ds_baidang

class DanhSachYeuThich(View):
    
    def get(self, request):
        user='admin'

        if request.GET.get('timkiem'):
            timkiem=request.GET.get('timkiem')
            ds_baidang=ds_yeuthich_timkiem(user,timkiem)  
        else:
            ds_baidang=ds_yeuthich_timkiem(user,None)  
        ds_baidang=tao_phan_trang(request,ds_baidang)
        
        if request.GET.get('timkiem'):
            return render(request,'main/ds_yeuthich.html',{'ds':ds_baidang,'timkiem':request.GET.get('timkiem')})
        return render(request,'main/ds_yeuthich.html',{'ds':ds_baidang})

    def post(self,request):
        user='admin'
        if not request.POST["timkiem"]:
            ds_baidang=ds_yeuthich_timkiem(user,None)
            ds_baidang=tao_phan_trang(request,ds_baidang)
            return render(request,'main/ds_yeuthich.html',{'ds':ds_baidang})
        timkiem=request.POST["timkiem"]
        ds_baidang=ds_yeuthich_timkiem(user,timkiem)
        ds_baidang=tao_phan_trang(request,ds_baidang)
        return render(request,'main/ds_yeuthich.html',{'ds':ds_baidang,'timkiem':timkiem})


def xem_chitiet(request,id_baidang):
    baidang=Baidang.objects.get(pk=id_baidang)
    if baidang.loai=='NHA':
        fh=Nha.objects.get(pk=id_baidang)
    else:
        fh=Chungcu.objects.get(pk=id_baidang)
    diachi='đường '+ baidang.diachi + ' phường '+baidang.huyen + ' quận ' +baidang.quan + ' tỉnh '+ baidang.tinh
    return render (request,'main/chitiet.html',{'baidang':baidang,'fh':fh,'diachi':diachi})

class GoBaiDang(View):
    def get(self,request,id_baidang):
        baidang=Baidang.objects.get(pk=id_baidang)
        return render(request,'main/go_baidang.html',{'baidang':baidang})
    
    def post(self,request,id_baidang):
        baidang=Baidang.objects.get(pk=id_baidang)
        ghinhan=request.POST["ghinhan"]
        if ghinhan=='daban':
            baidang.trangthai=2
        elif ghinhan =='khong':
            baidang.trangthai=3
        else:
            return render(request,'main/go_baidang.html',{'baidang':baidang,'message':'Vui lòng nhập chính xác mã xác nhận daban/khong'})
        baidang.save()
        return render(request,'main/go_baidang.html',{'message':'Thành công'})

def logout(request):
    return HttpResponse('logout')

def test(request):
    return render (request, template_name='main/test.html')



def unfollow(request,id_baidang):
    user='admin'
    
    try:
        yeuthich=DsYeuthich.objects.filter(tendangnhap=user, id_baidang=id_baidang)
        yeuthich.delete()
        ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where id_baidang in (SELECT id_baidang FROM DS_YEUTHICH where tendangnhap='"+user+"') and trangthai=1")
        return render(request,'main/ds_yeuthich.html',{'ds':ds_baidang,'message':'unfollow thành công'})
    except Exception as e:
        ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where id_baidang in (SELECT id_baidang FROM DS_YEUTHICH where tendangnhap='"+user+"') and trangthai=1")
        return render(request,'main/ds_yeuthich.html',{'ds':ds_baidang,'message':e})
    

class DanhSachDuyet(View):
    
    def get(self, request):
        ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where trangthai = 0")
        return render(request,'main/ds_duyet.html',{'ds':ds_baidang})

    def post(self,request):
        user='admin'
        if not request.POST["timkiem"]:
            
            ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where tendangnhap='"+user+"' and trangthai = 1")
            return render(request,'main/ds_baidang.html',{'ds':ds_baidang})
        timkiem=request.POST["timkiem"]
        if timkiem.isdigit():
            ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where tendangnhap = %s and trangthai = 1 and (id_baidang = %s "+
                                           "or ngaydang LIKE %s)",[user,timkiem,'%'+timkiem+'%'])
        else: 
            chuoi_chuan_hoa= str.upper(unidecode(timkiem))
            ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where tendangnhap= %s and trangthai = 1 and (tieude LIKE %s or loai LIKE %s)",[user,'%'+timkiem+'%','%'+chuoi_chuan_hoa+'%'])
        
        return render(request,'main/ds_baidang.html',{'ds':ds_baidang,'timkiem':timkiem})

class DuyetBaiDang(View):
    def get(self,request,id_baidang):
        f=Baidang.objects.get(pk=id_baidang)
        if f.loai=='NHA':
            fh=Nha.objects.get(pk=id_baidang)
        else:
            fh=Chungcu.objects.get(pk=id_baidang)
        if not f or not fh:
            return HttpResponse('Lỗi')
        
        return render(request,'main/duyet_baidang.html',{'f':f,'fh':fh})
    def post(self,request,id_baidang):
        f=Baidang.objects.get(pk=id_baidang)
        if f.loai=='NHA':
            fh=Nha.objects.get(pk=id_baidang)
        else:
            fh=Chungcu.objects.get(pk=id_baidang)
        if not f or not fh:
            return HttpResponse('Lỗi')
        try:
            button=request.POST['btn']
            if button=='Cho phép':
                f.trangthai=1
                f.save()
                return render(request,'main/thong_bao_duyet.html',{'message':'Đã cho phép đăng bài'})
            elif button=='Từ chối':
                for item in f.hinhanh_set.all():
                    item.delete()
                    print(item)
                fh.delete()
                f.delete()
                return render(request,'main/thong_bao_duyet.html',{'message':'Đã từ chối và xóa bài đăng'})
        except Exception as e:
            return render(request,'main/duyet_baidang.html',{'f':f,'fh':fh,'message':'Thao tác thất bại'})