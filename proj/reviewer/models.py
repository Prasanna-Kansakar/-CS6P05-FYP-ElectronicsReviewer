from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Accessories02Type(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Type")
    class Meta:
        verbose_name = "Accessory Type"
    def __str__(self):
        return self.name


class Accessories03Brand(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Brand Name")
    class Meta:
        verbose_name = "Accessory Brand"
    def __str__(self):
        return self.name
        
class Accessories05Price(models.Model):
    Daraz = 1
    SastoDeal = 2

    CHOICES = [
        (Daraz, 'Daraz'),
        (SastoDeal, 'SastoDeal')
    ]
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.URLField(max_length = 200)
    img_url = models.CharField(max_length=255)
    price = models.FloatField()
    type = models.SmallIntegerField(
        choices=CHOICES,
        default=SastoDeal
    )
    discount_price = models.FloatField()
    has_discount = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_updated = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Accessories01Accessories(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Accessories03Brand, on_delete=models.CASCADE)
    type = models.ForeignKey(Accessories02Type, on_delete=models.CASCADE)
    prices = models.ManyToManyField(Accessories05Price)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    feature = models.TextField()
    class Meta:
        ordering = ['-created_date']
    def __str__(self):
        return self.name
    def get_thumbnail(self):
        images = Accessories04images.objects.filter(accessory=self).first()
        return (images.img_url)
    def get_avg_rating(self):
        reviews = Reviews02Accessories_Review.objects.filter(accessory=self)
        count = len(reviews)
        sum = 0
        if not reviews.exists():
            return 0
        for rvw in reviews:
            sum += rvw.ratings
        return (sum/count)

class Accessories04images(models.Model):
    id = models.BigAutoField(primary_key=True)
    accessory = models.ForeignKey(Accessories01Accessories, on_delete=models.CASCADE)
    img_url = models.ImageField(upload_to ='images/accessories')

class Laptop02RAM(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="RAM")
    class Meta:
        verbose_name = "Laptop Ram"
    def __str__(self):
        return self.name


class Laptop03Brand(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Brand Name")
    class Meta:
        verbose_name = "Laptop Brand"
    def __str__(self):
        return self.name

class Laptop04Storage(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Storage")
    class Meta:
        verbose_name = "Laptop Storage"
    def __str__(self):
        return self.name

class Laptop05Processor(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Processor")
    class Meta:
        verbose_name = "Laptop Processor"
    def __str__(self):
        return self.name

class Laptop06GPU(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="GPU")
    vRAM = models.CharField(max_length=10, verbose_name="VRAM")
    class Meta:
        verbose_name = "Laptop GPU"
    def __str__(self):
        return f'{self.name} [{self.vRAM}]'

class Laptop07display(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Display")
    class Meta:
        verbose_name = "Laptop Display"
    def __str__(self):
        return self.name

class Laptop08OS(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Operating System")
    class Meta:
        verbose_name = "Laptop Operating System"
    def __str__(self):
        return self.name

class Laptop10Price(models.Model):
    Daraz = 1
    SastoDeal = 2
    CHOICES = [
        (Daraz, 'Daraz'),
        (SastoDeal, 'SastoDeal')
    ]
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.URLField(max_length = 200)
    price = models.FloatField()
    type = models.SmallIntegerField(
        choices=CHOICES,
        default=SastoDeal
    )
    discount_price = models.FloatField()
    has_discount = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_updated = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Laptop01Laptop(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    RAM = models.ManyToManyField(Laptop02RAM)
    brand = models.ForeignKey(Laptop03Brand, on_delete=models.CASCADE)
    storage = models.ManyToManyField(Laptop04Storage)
    processor = models.ManyToManyField(Laptop05Processor)
    gpu = models.ManyToManyField(Laptop06GPU)
    display = models.ManyToManyField(Laptop07display)
    os = models.ManyToManyField(Laptop08OS)
    feature = models.TextField()
    prices = models.ManyToManyField(Laptop10Price)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_date']
    def __str__(self):
        return self.name
    def get_thumbnail(self):
        images = Laptop09images.objects.filter(laptop=self)
        if images:
            return images.first().img_url
        else:
            return ""
    def get_avg_rating(self):
        reviews = Reviews01Laptop_Review.objects.filter(laptop=self)
        count = len(reviews)
        sum = 0
        if not reviews.exists():
            return 0
        for rvw in reviews:
            sum += rvw.ratings
        return (sum/count)

class Laptop09images(models.Model):
    id = models.BigAutoField(primary_key=True)
    laptop = models.ForeignKey(Laptop01Laptop, on_delete=models.CASCADE)
    img_url = models.ImageField(upload_to ='images/laptop')

class Blog01Blog(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    content = models.TextField()
    is_completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to ='images/blogs')
    class Meta:
        ordering = ['-created_date']
    def __str__(self):
        return self.title

class Bookmark01Laptop_Bookmark(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    laptop = models.ForeignKey(Laptop01Laptop, on_delete=models.CASCADE)

class Bookmark02Accessories_Bookmark(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accessory = models.ForeignKey(Accessories01Accessories, on_delete=models.CASCADE)

class Reviews01Laptop_Review(models.Model):
    id = models.BigAutoField(primary_key=True)
    ratings = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    laptop = models.ForeignKey(Laptop01Laptop, on_delete=models.CASCADE)
    content = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_date']

class Reviews02Accessories_Review(models.Model):
    id = models.BigAutoField(primary_key=True)
    ratings = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accessory = models.ForeignKey(Accessories01Accessories, on_delete=models.CASCADE)
    content = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_date']

class User01QRcode(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img_url = models.ImageField(upload_to ='images/qr')

class User02Verification(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grant_verfication = models.BooleanField(default=False)
    def getreviewscount(self):
        reviews = Reviews01Laptop_Review.objects.filter(user=self.user)
        reviews2 = Reviews02Accessories_Review.objects.filter(user=self.user)
        count = len(reviews) + len(reviews2)
        return (count)
