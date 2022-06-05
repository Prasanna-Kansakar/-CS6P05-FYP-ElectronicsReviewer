from cgi import test
from itertools import chain
from django.forms import formset_factory
from django.http import HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

from .tasks import AccessoryScraping, LaptopScraping, LaptopScraping2, send_mail_func
from .forms import BlogForm, CreateUserForm, AccessoryForm, AccessoryImageForm, LaptopImageForm, ReviewForm2, SearchAccessory, LaptopForm, ReviewForm1, SearchLaptop, comparelaptop
from .models import Accessories01Accessories, Accessories04images, Accessories05Price, Blog01Blog, Bookmark01Laptop_Bookmark, Bookmark02Accessories_Bookmark, Laptop01Laptop, Laptop09images, Laptop10Price, Reviews01Laptop_Review, Reviews02Accessories_Review, User02Verification
from django.contrib.auth import get_user_model, login, logout, authenticate
from .decorators import allowed_user, unauthenticated_user
from django.db.models import Subquery

@login_required(login_url='login')
@allowed_user(allowed_roles=['SuperAdmin'])
def scrap(request): 
    LaptopScraping.delay()
    LaptopScraping2.delay()
    AccessoryScraping.delay()
    return redirect('homepage') 

@login_required(login_url='login')
@allowed_user(allowed_roles=['SuperAdmin'])
def send_mail(request): 
    send_mail_func.delay()
    return redirect('homepage') 


def index(request):  
    blogs = Blog01Blog.objects.filter(is_completed=True, is_deleted=False)[:5]
    accessories = Accessories01Accessories.objects.filter(is_deleted=False)[:5]
    laptop = Laptop01Laptop.objects.filter(is_deleted=False)[:5]
    context = {'blog':blogs,
                'accessories': accessories,
                'laptop': laptop
                }
    return render(request,'index.html',context)  

@login_required(login_url='login')
@allowed_user(allowed_roles=['VerifiedUser'])
def blog(request):  
    blogs = Blog01Blog.objects.filter(author=request.user, is_deleted=False).order_by('created_date')
    context = {'blog':blogs}
    return render(request,'Blog/index.html',context)  

@login_required(login_url='login')
@allowed_user(allowed_roles=['VerifiedUser'])
def blog_create(request):
    if request.method == "POST":          
        form = BlogForm(request.POST, request.FILES or None)  
        if form.is_valid():  
            try:  
                blog = form.save(commit=False)
                blog.author = request.user
                blog.save()
                messages.add_message(request, messages.SUCCESS, 'Blog Sucessfully Added.')
                return redirect('blog index')
            except:  
                messages.add_message(request, messages.WARNING, 'Blog Couldnot be Added.')
                return redirect('blog create')
        else:
            return redirect('blog create')  
    else:  
        form = BlogForm()  
    context = {'form': form}
    return render(request,'Blog/Blog_create.html',context)  

@login_required(login_url='login')
@allowed_user(allowed_roles=['VerifiedUser'])
def blog_delete(request, id):
    blog = get_object_or_404(Blog01Blog,pk=id)  
    if blog.author!=request.user and blog.is_deleted!=False:
        messages.warning(request, "You do not have acess to the blog.")
        return redirect('blog index')
    if request.method == "POST": 
        blog = get_object_or_404(Blog01Blog,pk=request.POST.get('id'))
        if blog.author!=request.user and blog.is_deleted!=False:
            messages.warning(request, "You do not have acess to the blog.")
            return redirect('blog index')
        else:
            blog.is_deleted = True
            blog.save()
            messages.add_message(request, messages.SUCCESS, 'Blog Sucessfully Deleted.')
            return redirect('blog index')
    context = {'blog': blog}
    return render(request,'Blog/Blog_delete.html',context)  

@login_required(login_url='login')
@allowed_user(allowed_roles=['VerifiedUser'])
def blog_edit(request, id):
    blog = get_object_or_404(Blog01Blog,pk=id)
    if blog.author != request.user:
        messages.warning(request, "You do not have acess to the blog.")
        return redirect('blog index') 
    if request.method == "POST":  
        form = BlogForm(request.POST, request.FILES or None, instance=blog)
        if form.is_valid():  
            try:  
                form.save()  
                messages.add_message(request, messages.SUCCESS, 'Blog Sucessfully Edited.')
                return redirect('blog index')
            except:  
                messages.add_message(request, messages.WARNING, 'Blog Couldnot be Edited.')
                return redirect('blog index')  
    else:  
        form = BlogForm(instance=blog)  
    context = {'form': form}
    return render(request,'Blog/Blog_edit.html',context)  

@login_required(login_url='login')
@allowed_user(allowed_roles=['VerifiedUser'])
def blog_detail(request, id):
    blog = get_object_or_404(Blog01Blog,pk=id)  
    if blog.author==request.user and  blog.is_deleted==False:
        context = {'blog': blog}
        return render(request,'Blog/Blog_detail.html',context)
    else:
        messages.warning(request, "You do not have acess to the blog.")
        return redirect('blog index')
     

def blog_userview(request, id): 
    blog = get_object_or_404(Blog01Blog,pk=id)
    if blog.is_completed==True and  blog.is_deleted==False:
        context = {
            'blog': blog
        }
        return render(request,'Blog/Blog_single.html',context) 
    else:
        messages.warning(request, "The blog does not exist.")
        return redirect('blog user index')

def blog_list(request):  
    blogs = Blog01Blog.objects.filter(is_completed=True, is_deleted=False)
    page_num = request.GET.get('page', 1)
    paginator = Paginator(blogs, 5) 
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'Blog/Blog_list.html', {'page_obj': page_obj})

@unauthenticated_user
def user_login(request):  
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Sucessfully Logged in.')
            return redirect('homepage')
        else:
            messages.warning(request, 'Username OR password is incorrect')
    context = {}
    return render(request,'Accounts/login.html',context) 

@login_required(login_url='login')
def user_logout(request):  
    logout(request)
    messages.info(request, 'User Suceesfully logged out')
    return redirect('homepage')


@unauthenticated_user
def register(request):  
    if request.method == "POST":  
        form = CreateUserForm(request.POST)  
        if form.is_valid():  
            try:  
                user = form.save()
                group = Group.objects.get(name='User')
                user.groups.add(group)
                username = form.cleaned_data.get('username')
                messages.add_message(request, messages.SUCCESS, 'User: '+username+' Sucessfully Registered.')  
                return redirect('login')  
            except:  
                messages.warning(request,'User Couldnt be Created.')
    else:  
        form = CreateUserForm()  
    context = {'form':form}
    return render(request,'Accounts/register.html',context)  

@login_required(login_url='login')
@allowed_user(allowed_roles=['Admin'])
def laptop(request):  
    laptop = Laptop01Laptop.objects.filter(is_deleted=False).order_by('created_date')
    context = {'laptop': laptop}
    return render(request,'Laptop/index.html',context)  
 

@login_required(login_url='login')
@allowed_user(allowed_roles=['Admin'])
def laptop_create(request):  
    form = LaptopForm()
     
    if request.method == "POST":  
        form = LaptopForm(request.POST)
        iform = request.FILES.getlist('img_url')
        if form.is_valid():  
            try:
                if not iform:
                    messages.add_message(request, messages.WARNING, 'Please Add Images') 
                else:
                    laptop = form.save()
                    for image in iform:
                        img = Laptop09images(img_url = image)
                        img.laptop = laptop
                        img.save()
                    check = request.POST.getlist('check')
                    for c in check: 
                        price = Laptop10Price.objects.get(id=c) 
                        laptop.prices.add(price)                
                    messages.add_message(request, messages.SUCCESS, 'Laptop Sucessfully Added.') 
                    return redirect('laptop index')                  
            except:  
                messages.add_message(request, messages.WARNING, 'Laptop Couldnt be Added.') 
    iform = LaptopImageForm()  
    prices = Laptop10Price.objects.filter(is_deleted=False) 
    context = {'form':form,
                'iform':iform,
                'prices': prices}
    return render(request,'Laptop/Laptop_create.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['Admin'])
def laptop_delete(request,id):  
    laptop = get_object_or_404(Laptop01Laptop,pk=id)
    images = Laptop09images.objects.filter(laptop=laptop)   
    if request.method == "POST": 
        laptop = get_object_or_404(Laptop01Laptop,pk=request.POST.get('id'))    
        laptop.is_deleted = True
        laptop.save()
        messages.add_message(request, messages.SUCCESS, 'Laptop Sucessfully Deleted.')
        return redirect('laptop index')
    context = {'laptop': laptop,
                'images':images }
    return render(request,'Laptop/Laptop_delete.html',context)   

@login_required(login_url='login')
@allowed_user(allowed_roles=['Admin'])
def laptop_edit(request, id):  
    laptop = get_object_or_404(Laptop01Laptop,pk=id)
    image = Laptop09images.objects.filter(laptop = laptop)
    form = LaptopForm(instance=laptop) 
    if request.method == "POST":  
        form = LaptopForm(request.POST, instance=laptop)
        iform = request.FILES.getlist('img_url')
        if form.is_valid():  
            try:               
                laptop = form.save()
                if iform:
                    img = Laptop09images.objects.filter(laptop=laptop) 
                    for i in img:
                        i.delete()
                    for image in iform:
                        img = Laptop09images(img_url = image)
                        img.laptop = laptop
                        img.save()
                check = request.POST.getlist('check')
                print(check)
                if check:
                    laptop.prices.clear()                   
                    for c in check:
                        price = Laptop10Price.objects.get(id=c)
                        laptop.prices.add(price)                
                messages.add_message(request, messages.SUCCESS, ' Laptop Sucessfully Updated.') 
                return redirect('laptop index')                  
            except:  
                messages.add_message(request, messages.WARNING, 'Laptop Couldnt be Updated.') 
    iform = LaptopImageForm()   
    prices = Laptop10Price.objects.filter(is_deleted=False) 
    context = {'form':form,
                'iform':iform,
                'prices': prices}
    return render(request,'Laptop/Laptop_edit.html',context) 

@login_required(login_url='login')
@allowed_user(allowed_roles=['Admin'])
def laptop_detail(request, id):  
    laptop = get_object_or_404(Laptop01Laptop,pk=id)  
    images = Laptop09images.objects.filter(laptop=laptop)   
    context = {'laptop': laptop,
                'images':images }
    return render(request,'Laptop/Laptop_detail.html',context) 


def laptop_view(request,id):  
    laptop = get_object_or_404(Laptop01Laptop,pk=id)  
    images = Laptop09images.objects.filter(laptop=laptop) 
    reviews= Reviews01Laptop_Review.objects.filter(laptop=laptop)
    hasbookmarked = False
    if request.user.is_authenticated:
        User = request.user
        check = Bookmark01Laptop_Bookmark.objects.filter(user=User, laptop=laptop)
        if check.exists():
            hasbookmarked = True
        if request.method == "POST": 
            user = request.user 
            laptop = Laptop01Laptop.objects.get(id = id) 
            review = Reviews01Laptop_Review.objects.filter(laptop=laptop, user=user)
            form = ReviewForm1(request.POST)  
            if review:
                x = review.first()
                form = ReviewForm1(request.POST, instance=x)          
            if form.is_valid():  
                try:  
                    review = form.save(commit=False) 
                    review.user = user
                    review.laptop =laptop
                    review.ratings = request.POST.get('ratings')
                    review.save()                
                    messages.add_message(request, messages.SUCCESS, ' Review Sucessfully Added.')
                
                except:  
                    messages.add_message(request, messages.WARNING, ' Review Could not be Added.')                
    context = {'laptop': laptop,
                'images':images,
                'reviews': reviews,
                'hasbookmarked': hasbookmarked}
    return render(request,'Laptop/Laptop_single.html',context)  

def laptop_list(request):  
    laptop = Laptop01Laptop.objects.filter(is_deleted=False)
    images = []
    for item in laptop:
        image = Laptop09images.objects.filter(laptop=item).values('img_url')
        x = image[0]
        images.append(list(x.values())[0])
    nested_lst = [ laptop, images ]
    context = tuple( [tuple(l) for l in nested_lst])
    print(context)
    page_num = request.GET.get('page', 1)
    paginator = Paginator(context, 5) 
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request,'Laptop/Laptop_list.html', {'page_obj': page_obj}) 

@login_required(login_url='login')
@allowed_user(allowed_roles=['User', 'VerifiedUser','Admin'])
def bookmark_laptop(request,id):  
    User = request.user
    Laptop = Laptop01Laptop.objects.get(id =id)
    check = Bookmark01Laptop_Bookmark.objects.filter(user=User, laptop=Laptop)
    if check.exists():
        obj = check.first()
        obj.delete()
        messages.add_message(request, messages.WARNING, 'Bookmark Removed!')
    else:
        obj = Bookmark01Laptop_Bookmark(user=User, laptop=Laptop)
        obj.save()
        messages.add_message(request, messages.SUCCESS, 'Bookmark Added!')
    return redirect('laptop user view', id = id)

@login_required(login_url='login')
@allowed_user(allowed_roles=['User', 'VerifiedUser','Admin'])
def bookmark_accessory(request,id):  
    User = request.user
    Accessory = Accessories01Accessories.objects.get(id =id)
    check = Bookmark02Accessories_Bookmark.objects.filter(user=User, accessory=Accessory)
    if check.exists():
        obj = check.first()
        obj.delete()
        messages.add_message(request, messages.WARNING, 'Bookmark Removed!')
    else:
        obj = Bookmark02Accessories_Bookmark(user=User, accessory=Accessory)
        obj.save()
        messages.add_message(request, messages.SUCCESS, 'Bookmark Added!')
    return redirect('accessory user view', id = id)

@login_required(login_url='login')
@allowed_user(allowed_roles=['Admin'])
def accessory(request):  
    accessories = Accessories01Accessories.objects.filter(is_deleted=False).order_by('created_date')
    context = {'accessories': accessories}
    return render(request,'Accessory/index.html',context)  

@login_required(login_url='login')
@allowed_user(allowed_roles=['Admin'])
def accessory_create(request):
    form = AccessoryForm()
    iform = AccessoryImageForm()   
    if request.method == "POST":  
        form = AccessoryForm(request.POST)
        iform = request.FILES.getlist('img_url')
        if form.is_valid():  
            try:
                accessory = form.save()
                for image in iform:
                    img = Accessories04images(img_url = image)
                    img.accessory = accessory
                    img.save()
                check = request.POST.getlist('check')
                for c in check: 
                    price = Accessories05Price.objects.get(id=c) 
                    accessory.prices.add(price)                
                messages.add_message(request, messages.SUCCESS, ' Accessory Sucessfully Added.') 
                return redirect('accessory index')                  
            except:  
                messages.add_message(request, messages.WARNING, 'Accessory Couldnt be Added.')  
    prices = Accessories05Price.objects.filter(is_deleted=False) 
    context = {'form':form,
                'iform':iform,
                'prices': prices}
    return render(request,'Accessory/Accessory_create.html',context)  

@login_required(login_url='login')
@allowed_user(allowed_roles=['Admin'])
def accessory_delete(request,id):
    Accessory = get_object_or_404(Accessories01Accessories,pk=id)
    images = Accessories04images.objects.filter(accessory=Accessory)   
    if request.method == "POST": 
        accessory = get_object_or_404(Accessories01Accessories,pk=request.POST.get('id'))    
        accessory.is_deleted = True
        accessory.save()
        messages.add_message(request, messages.SUCCESS, 'Accessory Sucessfully Deleted.')
        return redirect('accessory index')
    context = {'accessory': Accessory,
                'images':images }
    return render(request,'Accessory/Accessory_delete.html',context)  

@login_required(login_url='login')
@allowed_user(allowed_roles=['Admin'])
def accessory_edit(request,id):  
    accessory = get_object_or_404(Accessories01Accessories,pk=id)
    image = Accessories04images.objects.filter(accessory = accessory)
    form = AccessoryForm(instance=accessory)
    iform = AccessoryImageForm()   
    if request.method == "POST":  
        form = AccessoryForm(request.POST, instance=accessory)
        iform = request.FILES.getlist('img_url')
        if form.is_valid():  
            try:               
                accessory = form.save()
                if iform:
                    img = Accessories04images.objects.filter(accessory=accessory) 
                    for i in img:
                        i.delete()
                    for image in iform:
                        img = Accessories04images(img_url = image)
                        img.accessory = accessory
                        img.save()
                check = request.POST.getlist('check')
                print(check)
                if check:
                    accessory.prices.clear()                   
                    for c in check:
                        price = Accessories05Price.objects.get(id=c)
                        accessory.prices.add(price)                
                messages.add_message(request, messages.SUCCESS, ' Accessory Sucessfully Updated.') 
                return redirect('accessory index')                  
            except:  
                messages.add_message(request, messages.WARNING, 'Accessory Couldnt be Updated.')  
    prices = Accessories05Price.objects.filter(is_deleted=False) 
    context = {'form':form,
                'iform':iform,
                'prices': prices}
    return render(request,'Accessory/Accessory_edit.html',context)  

@login_required(login_url='login')
@allowed_user(allowed_roles=['Admin'])
def accessory_detail(request,id):
    Accessory = get_object_or_404(Accessories01Accessories,pk=id)  
    images = Accessories04images.objects.filter(accessory=Accessory)   
    context = {'accessory': Accessory,
                'images':images }
    return render(request,'Accessory/Accessory_detail.html',context) 


def accessory_view(request,id):  
    Accessory = get_object_or_404(Accessories01Accessories,pk=id)  
    images = Accessories04images.objects.filter(accessory=Accessory) 
    reviews= Reviews02Accessories_Review.objects.filter(accessory=Accessory)
    hasbookmarked = False
    if request.user.is_authenticated:
        User = request.user
        check = Bookmark02Accessories_Bookmark.objects.filter(user=User, accessory=Accessory)
        if check.exists():
            hasbookmarked = True
        if request.method == "POST": 
            user = request.user 
            accessory = Accessories01Accessories.objects.get(id = id) 
            review = Reviews02Accessories_Review.objects.filter(accessory=accessory, user=user)
            form = ReviewForm2(request.POST)  
            if review:
                x = review.first()
                form = ReviewForm2(request.POST, instance=x)          
            if form.is_valid():  
                try:  
                    review = form.save(commit=False) 
                    review.user = user
                    review.accessory =accessory
                    review.ratings = request.POST.get('ratings')
                    review.save()                
                    messages.add_message(request, messages.SUCCESS, ' Review Sucessfully Added.')
                
                except:  
                    messages.add_message(request, messages.WARNING, ' Review Could not be Added.')                
    context = {'accessory': Accessory,
                'images':images,
                'reviews': reviews,
                'hasbookmarked': hasbookmarked}
    return render(request,'Accessory/Accessory_single.html',context)  


def accessory_list(request):  
    Accessory = Accessories01Accessories.objects.filter(is_deleted=False)
    images = []
    for item in Accessory:
        image = Accessories04images.objects.filter(accessory=item).values('img_url')
        x = image[0]
        images.append(list(x.values())[0])
    nested_lst = [ Accessory, images ]
    context = tuple( [tuple(l) for l in nested_lst])
    print(context)
    page_num = request.GET.get('page', 1)
    paginator = Paginator(context, 5) 
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request,'Accessory/Accessory_list.html', {'page_obj': page_obj}) 

def search_panel(request):
    accessory = Accessories01Accessories.objects.filter(is_deleted=False)[:5]  
    if request.method == "POST":
        accessory = Accessories01Accessories.objects.filter(is_deleted=False)  
        form = SearchAccessory(request.POST)  
        if form['name'].value():
            accessory = accessory.filter( name__icontains=form['name'].value())
        if form['type'].value():
            accessory = accessory.filter( type=form['type'].value())
        if form['brand'].value():
            accessory = accessory.filter(brand=form['brand'].value())
        print(accessory)
    else:  
        form = SearchAccessory()  
    context = {'accessory':accessory,
                'form':form}
    return render(request,'Accessory/Accessory_search.html',context)  

@login_required(login_url='login')
@allowed_user(allowed_roles=['User', 'VerifiedUser', 'Admin'])
def laptop_review(request, id):  
    user = request.user 
    laptop = Laptop01Laptop.objects.get(id = id) 
    form = ReviewForm1()       
    rating = 1        
    review = Reviews01Laptop_Review.objects.filter(laptop=laptop, user=user)
    if review:
        x = review.first()
        form = ReviewForm1(instance=x)
        rating = x.ratings
    context = {'form': form,
                'rating': rating}
    return render(request,'Laptop/Laptop_review.html',context)  

@login_required(login_url='login')
@allowed_user(allowed_roles=['User', 'VerifiedUser', 'Admin'])
def accessory_review(request, id):
    user = request.user 
    accessory = Accessories01Accessories.objects.get(id = id) 
    form = ReviewForm2()       
    rating = 1        
    review = Reviews02Accessories_Review.objects.filter(accessory=accessory, user=user)
    if review:
        x = review.first()
        form = ReviewForm2(instance=x)
        rating = x.ratings
    context = {'form': form,
                'rating': rating}
    return render(request,'Accessory/Accessory_review.html',context) 

def compare(request): 
    FormSet = formset_factory(comparelaptop, extra=2)
    context = {'formset':FormSet}
    return render(request,'Laptop/Laptop_compare.html',context)  


def ajax_compare(request,id):  
    laptop = Laptop01Laptop.objects.get(id = id) 
    context = {'laptop':laptop}
    return render(request,'shared/Laptop_compare.html',context)  

@login_required(login_url='login')
@allowed_user(allowed_roles=['Admin'])
def verify(request):  
    users = User02Verification.objects.all()
    context = {'users':users}
    return render(request,'Accounts/verify.html',context)  

@login_required(login_url='login')
@allowed_user(allowed_roles=['User'])
def verify_user(request):
    User = request.user
    obj = User02Verification.objects.filter(user=User)
    if obj: 
        messages.add_message(request, messages.WARNING, ' Request for Verification has Already been Sent.')   
    else:
        x = User02Verification(user=User)
        x.save()
        messages.add_message(request, messages.SUCCESS, ' Request for Verification has been Sent.')  
    return redirect('homepage') 

@login_required(login_url='login')
@allowed_user(allowed_roles=['User', 'VerifiedUser', 'Admin'])
def bookmark_list(request):
    user = request.user
    laptop  = Bookmark01Laptop_Bookmark.objects.filter(user=user)
    accessory = Bookmark02Accessories_Bookmark.objects.filter(user=user)
    context = {
        'laptop': laptop,
        'accessory':accessory
    }
    return render(request,'Accounts/My_Bookmarks.html',context)  

def laptop_search_panel(request):  
    laptop = Laptop01Laptop.objects.filter(is_deleted=False)[:5]  
    if request.method == "POST":
        form = SearchLaptop(request.POST)  
        laptop = Laptop01Laptop.objects.filter(is_deleted=False)
        if form.is_valid():
            if form['name'].value():
                laptop = laptop.filter( name__icontains=form['name'].value())
            if form['brand'].value():
                laptop = laptop.filter(brand=form['brand'].value())
            a = form.cleaned_data['RAM']
            if a:
                laptop = laptop.filter( RAM__in=a)
            a = form.cleaned_data['storage']
            if a:
                laptop = laptop.filter( storage__in=a) 
            a = form.cleaned_data['processor']
            if a:
                laptop = laptop.filter( processor__in=a) 
            a = form.cleaned_data['gpu']
            if a:
                laptop = laptop.filter( gpu__in=a) 
            a = form.cleaned_data['display']
            if a:
                laptop = laptop.filter( display__in=a) 
            a = form.cleaned_data['os']
            if a:
                laptop = laptop.filter( os__in=a)           
    else:  
        form = SearchLaptop()  
    context = {'laptop':laptop,
                'form':form}
    return render(request,'Laptop/Laptop_search.html',context)  


@login_required(login_url='login')
@allowed_user(allowed_roles=['Admin'])
def confirm_verification(request,id):
    user = get_user_model().objects.get(id = id)
    user.groups.clear()
    group = Group.objects.get(name='VerifiedUser')
    user.groups.add(group)
    obj = User02Verification.objects.filter(user=user)
    x = obj.first() 
    x.delete()
    messages.add_message(request, messages.SUCCESS, ' User Verified.')  
    return redirect('verify') 