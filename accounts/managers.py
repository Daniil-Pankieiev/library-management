from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.is_active = is_active
        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, password, email=None, **extra_fields):
        if email:
            email = self.normalize_email(email)
        user = self.create_user(email=email, password=password, **extra_fields)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user
