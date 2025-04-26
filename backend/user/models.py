from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class Role(models.Model):
    """
        Admin/Staff/Customer/...

    """
    name = models.CharField(max_length=50, unique=True)  # Admin, Staff, Customer
    permissions = models.JSONField(default=dict)  # Lưu quyền chi tiết
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class User(AbstractUser):
    """
    Đại diện cho người dùng trong hệ thống (Admin, Staff, Technician, Customer).
    """
    full_name = models.CharField(max_length=50, blank=True)     # ho ten

    email = models.EmailField(unique=True)      # email unique

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)    # vai tro : admin/staff/...

    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)   # so du tai khoan

    # override liên kết groups
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    # override liên kết permission
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
