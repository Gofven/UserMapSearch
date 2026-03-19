from django.contrib.gis.geos import Point, Polygon
from ninja import Schema, Query, Field
from ninja.errors import ValidationError, HttpError
from ninja.pagination import paginate

from backend.api import api
from mapsearch.user.models import User


class UserSchema(Schema):
    email: str
    latitude: float = Field(None, alias='location_point.y')
    longitude: float = Field(None, alias='location_point.x')


class UserRegisterSchema(UserSchema):
    password: str


class UserLoginSchema(Schema):
    email: str
    password: str


# We'll assume we always use "srid = 4326"
class PointSchema(Schema):
    latitude: float
    longitude: float


class BoundingBoxSchema(Schema):
    min_latitude: float = None
    min_longitude: float = None
    max_latitude: float = None
    max_longitude: float = None


class UserListSchema(Schema):
    user_id: int = None
    bounding_box: BoundingBoxSchema = None


@api.get("/user", tags=['user'], response=UserSchema)
async def get_user(request):
    return request.auth


@api.get("/user/list", tags=['user'], response=list[UserSchema])
@paginate
async def user_list(request, user_list_schema: Query[UserListSchema]):
    bbox = user_list_schema.bounding_box

    # I was unable to find any django-ninja native solution to this (aside from this or making a custom handler)
    if all([x is not None for x in bbox.dict().values()]):
        bounding_box = Polygon.from_bbox([bbox.min_longitude,
                                          bbox.min_latitude,
                                          bbox.max_longitude,
                                          bbox.max_latitude])

    elif any([x is not None for x in bbox.dict().values()]):
        raise HttpError(400, "Missing fields for Bounding Box.")

    else:
        bounding_box = None


    filters = dict(user_list_schema.dict(exclude_unset=True, exclude=['bounding_box']))

    if bounding_box:
        filters['location_point__within'] = bounding_box

    return User.objects.filter(**filters)


@api.post("/register", tags=['user'], auth=None)
async def register(request, user_details: UserRegisterSchema):
    user = await User.objects.acreate_user(**user_details.dict())
    return UserSchema(email=user.email)


@api.post("/login", tags=['user'], auth=None)
async def login(request, login_details: UserLoginSchema):
    try:
        user = await User.objects.aget(email=login_details.email)

    except User.DoesNotExist:
        raise ValidationError([{"email": "Email does not exist"}])

    if not await user.acheck_password(raw_password=login_details.password):
        raise ValidationError([{"password": "Password is incorrect"}])

    return user.api_key


@api.post("/map/location/get", tags=['map'], response=PointSchema)
async def get_location(request):
    point = request.auth.location_point
    return dict(latitude=point.y, longitude=point.x)


@api.post("/map/location/update", tags=['map'])
async def update_location(request, location: PointSchema):
    request.auth.location_point = Point(location.longitude, location.latitude, srid=4326)
    await request.auth.asave()
