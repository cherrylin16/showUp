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

    phone = models.CharField(max_length=20, blank=True, null=True, db_column="phone")
    birthdate = models.DateField(blank=True, null=True, db_column="birthdate")
    accountCreated = models.DateTimeField(auto_now_add=True, db_column="accountCreated")

    pfp = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
        db_column="pfp"
    )

    preferenceID = models.IntegerField(blank=True, null=True, db_column="preferenceID")

    # Required for Django auth/admin
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = ShowUpUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstName", "lastName"]

    class Meta:
        db_table = "ShowUp_Users"

    def __str__(self):
        return self.email