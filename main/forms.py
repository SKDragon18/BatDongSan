from django import forms
from .models import Baidang, Nha, Chungcu
from django.forms import ModelForm
class BaiDangForm(ModelForm):
    loai=forms.ChoiceField(
            widget=forms.RadioSelect(attrs={'class':'form-check-label'}),
            choices=[
                    ('NHA', 'Nhà ở'),
                    ('CHUNGCU', 'Chung cư'),
                    ]
                    
        )
    chudang=forms.ChoiceField(
            widget=forms.RadioSelect(attrs={'class':'form-check-label'}),
            choices=[
                    ('cá nhân', 'Cá nhân'),
                    ('môi giới', 'Môi giới'),
                    ]
                    
        )
    class Meta:
        model=Baidang
        fields=['id_baidang','tieude','loai','diachi','huyen','quan','tinh',
                'giayto', 'sopn','tinhtrang','dientich','dai','rong','giaban','chitiet',
                'chudang','ngaydang']
        
        widgets={
            'id_baidang':forms.NumberInput(attrs={'class':'form-control'}),
            'tieude':forms.TextInput(attrs={'class':'form-control'}),
            'chitiet':forms.Textarea(attrs={'class':'form-control','id':'textarea','placeholder':'Thông tin chi tiết...','rows':'7'}),
            'diachi':forms.TextInput(attrs={'class':'form-control','placeholder':'Nhập địa chỉ đường'}),
            'huyen': forms.TextInput(attrs={'class':'form-control'}),
            'quan':forms.TextInput(attrs={'class':'form-control'}),
            'tinh':forms.TextInput(attrs={'class':'form-control'}),
            'giayto':forms.CheckboxInput(attrs={'class':'form-check-input','id':"flexSwitchCheckDefault"}),
            'sopn':forms.NumberInput(attrs={'class':'form-control','min':'1'}),
            'tinhtrang':forms.TextInput(attrs={'class':'form-control'}),
            'dai':forms.NumberInput(attrs={'class':'form-control','min':'1'}),
            'rong':forms.NumberInput(attrs={'class':'form-control','min':'1'}),
            'dientich':forms.NumberInput(attrs={'class':'form-control','min':'1'}),
            'giaban':forms.NumberInput(attrs={'class':'form-control','min':'1000000'}),
            'ngaydang':forms.DateInput(attrs={'class':'form-control'})
        }
        
        # fields='__all__'
        
class NhaForm(ModelForm):
    class Meta:
        model=Nha
        fields=['sotang','loaihinh']
        widgets={
            'sotang':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
            'loaihinh':forms.TextInput(attrs={'class':'form-control'})
        }

class ChungCuForm(ModelForm):
    class Meta:
        model=Chungcu
        fields=['lo','macan','sotang','huong']
        widgets={
            'lo':forms.TextInput(attrs={'class':'form-control'}),
            'macan':forms.TextInput(attrs={'class':'form-control'}),
            'sotang':forms.NumberInput(attrs={'class':'form-control','min':'0'}),
            'huong':forms.TextInput(attrs={'class':'form-control'})
        }

