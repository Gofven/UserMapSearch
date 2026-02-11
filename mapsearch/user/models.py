import secrets

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models, IntegrityError
from ninja.errors import ValidationError


class CustomUserManager(BaseUserManager):
    async def acreate_user(self, email: str, password: str):
        email = self.normalize_email(email)
        user = self.model(email=email)

        # No need for password validators for this project (to allow quick 1-letter password for testing)
        user.set_password(password)

        try:
            await user.asave()

        except IntegrityError:  # The only error that can occur in this case is that email already exists.
            raise ValidationError([{"email": "Email already exists"}])

        return user


def generate_api_key():
    return secrets.token_urlsafe(16)


# A simple user with email is all that's needed for this project
class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=120)
    api_key = models.CharField(max_length=128, default=generate_api_key)

    objects = CustomUserManager()
