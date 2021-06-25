from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),  #even if capital lettered email is entered it's normalized to default lowercase
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password) #inbuilt function
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):

        #we user create_user method to create superuser

        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name= last_name,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)


    #required fields
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()    #reference to the above class to be used to acontrol/manage accounts

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)  #unique one profile for one account
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    city = models.CharField(blank=True, max_length=100)
    state = models.CharField(blank=True, max_length=100)
    country = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.address_line_1}, {self.address_line_2}'
    