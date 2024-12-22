from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,Group, Permission
# Create your models here.

#https://docs.djangoproject.com/en/5.1/topics/auth/customizing/
class AccountManager(BaseUserManager):
    def create_account(self,email,username,password=None,**extra_fields):
        if not email:
            raise ValueError("Users must have an Email Address")
        if not username:
            raise ValueError("User must have an Username")
        
        if not password:
            raise ValueError("User must have a Password")
        email = self.normalize_email(email)
        user = self.model(email = email,username = username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,username,password=None, **extra_fields):
        extra_fields.setdefault("is_admin",True)
        return self.create_account(email,username,password,**extra_fields)
    

class Account(AbstractBaseUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    DEPARTMENT_CHOICES = [
        ('Computing', 'Computing'),
        ('Business', 'Business'),
        ('Engineering', 'Engineering'),
        ('Others', 'Others'),
    ]
    username = models.CharField(max_length=10,unique=True,null = False)
    email = models.EmailField(verbose_name="Email Address",max_length=255,unique=True,null=False)
    Fname = models.CharField(max_length = 25,null = False,verbose_name="First Name")
    Mname = models.CharField(max_length = 25,null=True, blank = True,verbose_name= "Middle Name")
    Lname = models.CharField(max_length = 25,null = False,verbose_name="Last Name")
    bio = models.TextField(blank=True,null = True,max_length=150,verbose_name="Basic Info")
    department = models.CharField(choices=DEPARTMENT_CHOICES,max_length=50)#need to check with the departments
    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    Gender = models.CharField(choices = GENDER_CHOICES,max_length=1)
    staff = models.BooleanField(default = False)#store lecturers,dean and others
    dob = models.DateField(null = False)
    dp = models.CharField(default = "avatar.png",null = True)
    role = models.CharField(max_length=50,default = 'Student')
    Address = models.CharField(max_length = 255)
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customaccount_permissions", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','Fname','Lname']

    objects = AccountManager()

    def __str__(self):
        return 'Email = ' + self.email + ', Username = ' + self.username
    
    def get_full_name(self):
        if self.Mname:
            return f'{self.Fname} {self.Mname} {self.Lname}'
        return f'{self.Fname} {self.Lname}'
    
    def has_perm(self,perm,obj = None):
        return True
    
    @property
    def is_Admin(self):
        return self.is_admin



    
    
    
