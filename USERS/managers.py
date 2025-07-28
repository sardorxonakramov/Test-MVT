from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("Email address is required")
        if not phone:
            raise ValueError("Phone number is required")
        if not first_name:
            raise ValueError("First name is required")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin") 


        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, first_name, phone, password, **extra_fields)