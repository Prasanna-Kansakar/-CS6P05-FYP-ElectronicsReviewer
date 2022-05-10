import email
from msilib.schema import Class
from tkinter import Widget
from django.forms import ModelForm, Form
from django import forms
from .models import Accessories01Accessories, Accessories02Type, Accessories03Brand, Accessories04images, Blog01Blog, Laptop01Laptop, Laptop02RAM, Laptop03Brand, Laptop04Storage, Laptop05Processor, Laptop06GPU, Laptop07display, Laptop08OS, Laptop09images, Reviews02Accessories_Review, Reviews01Laptop_Review, User02Verification
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    username = forms.CharField(label="Username", required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username..'}))
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email..'}))
    password1 = forms.CharField(label="Password", required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Enter password...'}))
    password2 = forms.CharField(label="Confirm Password", required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Re-enter Password...'}))
    class Meta:
         model = User
         fields = ['username', 'email', 'password1','password2']
    

class LaptopForm(ModelForm):
    class Meta:
        model = Laptop01Laptop
        fields = ['name', 'RAM', 'brand', 'storage', 'processor', 'gpu', 'display', 'os', 'feature']
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-control select2-single'}),
            'RAM': forms.SelectMultiple(attrs={'class': 'form-control select2-single'}),
            'storage': forms.SelectMultiple(attrs={'class': 'form-control select2-single'}),
            'processor': forms.SelectMultiple(attrs={'class': 'form-control select2-single'}),
            'gpu': forms.SelectMultiple(attrs={'class': 'form-control select2-single'}),
            'display': forms.SelectMultiple(attrs={'class': 'form-control select2-single'}),
            'os': forms.SelectMultiple(attrs={'class': 'form-control select2-single'})
        }
    name = forms.CharField(max_length=255,label="Name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter the Name of the Laptop'}), required=True)
    feature = forms.CharField(label="Features", widget=forms.Textarea(attrs={ 'rows': 30, 'class':'col-md-10' ,'id':'editor' }))

class LaptopImageForm(ModelForm):
    class Meta:    
        model = Laptop09images
        fields = ['img_url']
    img_url = forms.ImageField(label="Images", required=False, widget=forms.FileInput(attrs={'class':'form-control-file','multiple':True}))

class AccessoryImageForm(ModelForm):
    class Meta:    
        model = Accessories04images
        fields = ['img_url']
    img_url = forms.ImageField(label="Images", required=False, widget=forms.FileInput(attrs={'class':'form-control-file','multiple':True}))

class SearchLaptop(ModelForm):
    class Meta:
        model = Laptop01Laptop
        fields = ['name', 'RAM', 'brand', 'storage', 'processor', 'gpu', 'display', 'os']
    name = forms.CharField(max_length=255,label="Name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter the Laptop name'}), required=False)
    brand = forms.ModelChoiceField(queryset=Laptop03Brand.objects.all(), required=False,
                    label='Brand',
                    widget=forms.Select(attrs={'class': 'form-control select2-single'}),)
    RAM = forms.ModelMultipleChoiceField(queryset=Laptop02RAM.objects.all(), required=False,
                    label='RAM',
                    widget=forms.SelectMultiple(attrs={'class': 'form-control select2-single'}))
    storage = forms.ModelMultipleChoiceField(queryset=Laptop04Storage.objects.all(), required=False,
                    label='Storage',
                    widget=forms.SelectMultiple(attrs={'class': 'form-control select2-single'}))
    processor = forms.ModelMultipleChoiceField(queryset=Laptop05Processor.objects.all(), required=False,
                    label='Processor',
                    widget=forms.SelectMultiple(attrs={'class': 'form-control select2-single'}),)
    gpu = forms.ModelMultipleChoiceField(queryset=Laptop06GPU.objects.all(), required=False,
                    label='GPU',
                    widget=forms.SelectMultiple(attrs={'class': 'form-control select2-single'}))
    display = forms.ModelMultipleChoiceField(queryset=Laptop07display.objects.all(), required=False,
                    label='Display',
                    widget=forms.SelectMultiple(attrs={'class': 'form-control select2-single'}))
    os = forms.ModelMultipleChoiceField(queryset=Laptop08OS.objects.all(), required=False,
                    label='OS',
                    widget=forms.SelectMultiple(attrs={'class': 'form-control select2-single'}))


class SearchAccessory(ModelForm):
    class Meta:
        model = Accessories01Accessories
        fields = ['name', 'brand', 'type']
    name = forms.CharField(max_length=255,label="Name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter the Accessory name'}), required=False)
    brand = forms.ModelChoiceField(queryset=Accessories03Brand.objects.all(), required=False,
                    label='Brand',
                    widget=forms.Select(attrs={'class': 'form-control select2-single'}),)
    type = forms.ModelChoiceField(queryset=Accessories02Type.objects.all(), required=False,
                    label='Type',
                    widget=forms.Select(attrs={'class': 'form-control select2-single'}))

class AccessoryForm(ModelForm):
    class Meta:
    
        model = Accessories01Accessories
        fields = ['name', 'brand', 'type', 'feature']
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-control select2-single'}),
            'type': forms.Select(attrs={'class': 'form-control select2-single'}),
        }
    name = forms.CharField(max_length=255,label="Name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter the Accessory name'}), required=True)
    feature = forms.CharField(label="Features", widget=forms.Textarea(attrs={ 'rows': 30, 'class':'col-md-10' ,'id':'editor'}))

class ReviewForm1(ModelForm):
    class Meta:
        model = Reviews01Laptop_Review
        fields = ['content']
    content= forms.CharField(label="Review", widget=forms.Textarea(attrs={ 'rows': 10, 'class':'col-md-12','placeholder': 'Enter the Review' }))

class ReviewForm2(ModelForm):
    class Meta:
        model = Reviews02Accessories_Review
        fields = ['content']
    content= forms.CharField(label="Review", widget=forms.Textarea(attrs={ 'rows': 10, 'class':'col-md-12','placeholder': 'Enter the Review' }))

PUBLISH = [ (True, 'Publish'), (False, 'Save as Draft')]
class BlogForm(ModelForm):
    class Meta:
        model = Blog01Blog
        fields = ['title', 'description', 'content','is_completed','thumbnail']
    title = forms.CharField(max_length=100,label="Title", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter the Title of the Blog'}), required=True)
    description = forms.CharField(max_length=255,label="Short Description", widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter the Description of the Blog'}), required=True)
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={ 'rows': 30, 'class':'col-md-10' ,'id':'editor' }))
    is_completed = forms.ChoiceField(
                    choices = PUBLISH,
                    label='Action',
                    required=True,
                    widget=forms.Select(attrs={'class': 'form-control select2-single'}),
                    )
    thumbnail = forms.ImageField(label="Thumbnail")

class comparelaptop(Form):
    name = forms.ModelChoiceField(queryset=Laptop01Laptop.objects.filter(is_deleted=False), required=True, widget=forms.Select(attrs={'class': 'form-control select2-single compare'}),)
