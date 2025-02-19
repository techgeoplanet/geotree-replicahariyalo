from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

#  Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, department, user_department, distinations, mobilenumber, tc, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            department=department,
            mobilenumber=mobilenumber,
            user_department=user_department,
            distinations=distinations,
            tc=tc,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, department, user_department, distinations, mobilenumber, tc, password=None, **extra_fields):
        user = self.create_user(
            email,
            name=name,
            department=department,
            mobilenumber=mobilenumber,
            user_department=user_department,
            distinations=distinations,
            tc=tc,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True  # Make sure the user is marked as a superuser
        user.save(using=self._db)
        
        # Assign all permissions to the superuser
        from django.contrib.auth.models import Permission
        permissions = Permission.objects.all()
        user.user_permissions.set(permissions)
        user.save(using=self._db)
        
        return user


#  Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=100, blank=True)
    user_department = models.CharField(max_length=100, blank=True)
    distinations = models.CharField(max_length=100, blank=True)
    mobilenumber = models.CharField(max_length=10)
    tc = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'department', 'tc','user_department','mobilenumber','distinations']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_partner(self):
        return self.is_active

    class Meta:
        permissions = [
            ('can_manage_users', 'Can manage users'),
        ]





# Temp User Manager
class TempUserManager(BaseUserManager):
    def create_user(self, phone):
        if not phone:
            raise ValueError('Users must have a phone number')
        
        user = self.model(phone=phone)
        user.save(using=self._db)
        return user

# Temp User Model
class TempUser(AbstractBaseUser):
    phone = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = TempUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.phone
    

class UserDistrictPermissions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    district = models.ForeignKey('portaldash.DistrictList', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)  # Corrected `false` to `False`

    def __str__(self):
        return f"{self.user.email} - {self.district.DISTRICT_N} ({'Active' if self.status else 'Inactive'})"
