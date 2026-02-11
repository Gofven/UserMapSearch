from ninja import Schema
from ninja.errors import ValidationError

from backend.api import api
from mapsearch.user.models import User


class UserSchema(Schema):
    email: str


class UserRegisterSchema(UserSchema):
    password: str


class UserLoginSchema(Schema):
    email: str
    password: str


@api.post("/register")
async def register(request, user_details: UserRegisterSchema, auth=None):
    user = await User.objects.acreate_user(**user_details.dict())
    return UserSchema(email=user.email)


@api.post("/login")
async def login(request, login_details: UserLoginSchema, auth=None):
    try:
        user = await User.objects.aget(email=login_details.email)

    except User.DoesNotExist:
        raise ValidationError([{"email": "Email does not exist"}])

    if not await user.acheck_password(raw_password=login_details.password):
        raise ValidationError([{"password": "Password is incorrect"}])

    return user.api_key
