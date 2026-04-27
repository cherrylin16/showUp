from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class ShowUpUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hashes password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


class ShowUpUser(AbstractBaseUser, PermissionsMixin):
    userID = models.AutoField(primary_key=True, db_column="userID")

    firstName = models.CharField(max_length=100, db_column="firstName")
    lastName = models.CharField(max_length=100, db_column="lastName")
    email = models.EmailField(unique=True, db_column="email")

    phone = models.CharField(max_length=255)  
    birthdate = models.DateField()            

    pfp = models.BinaryField(null=True, blank=True) 

    accountCreated = models.DateTimeField(auto_now_add=True, db_column="accountCreated")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    preference = models.ForeignKey(
        "Preference",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="preferenceID"
    )


    objects = ShowUpUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstName", "lastName"]

    class Meta:
        db_table = "ShowUp_Users"
        managed = False

    def __str__(self):
        return self.email
    
    
class Preference(models.Model):
    preferenceID = models.AutoField(primary_key=True, db_column="preferenceID")

    lightMode = models.CharField(max_length=10, db_column="lightMode")
    notifications = models.BooleanField(db_column="notifications")

    class Meta:
        db_table = "ShowUp_Preferences"
        managed = False

    def __str__(self):
        return f"{self.lightMode}, notifications={'On' if self.notifications else 'Off'}"