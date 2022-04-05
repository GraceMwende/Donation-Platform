from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django_resized import ResizedImageField
from PIL import Image
from cloudinary.models import CloudinaryField

# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, user_name, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, user_name= user_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, user_name, password, **extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    is_charity = models.BooleanField(default=False)
    is_donor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    user_name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    last_name = models.CharField(max_length=150,default='Mwende')
    first_name = models.CharField(max_length=150, default='Grace')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Charity(models.Model):
    charity = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    location = models.CharField(max_length=150,default='Nairobi')
    # charity_image = models.ImageField(upload_to = 'charities/' , default='default.jpg',blank=True, null=True)
    charity_image=CloudinaryField('image',blank=True,null=True)

    def __str__(self):
        return self.charity.user_name

    # def save(self):
    #     if not self.charity_image:
    #         return            

    #     super(Charity, self).save()
    #     image = Image.open(self.charity_image)
    #     (width, height) = image.size     
    #     size = ( 600, 600)
    #     image = image.resize(size, Image.ANTIALIAS)
    #     image.save(self.charity_image.path)

class BenefactorsStory(models.Model):
    user_image = CloudinaryField('image',blank=True,null=True)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=30)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # def save(self):
    #     if not self.user_image:
    #         return            

    #     super(BenefactorsStories, self).save()
    #     image = Image.open(self.user_image)
    #     (width, height) = image.size     
    #     size = ( 600, 600)
    #     image = image.resize(size, Image.ANTIALIAS)
    #     image.save(self.user_image.path)

class Donor(models.Model):
    donor = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.donor.user_name

class Donations(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.donor.donor.user_name
