"""API routes for users app."""
from django.core.handlers.wsgi import WSGIRequest
from ninja import Router
from ninja_jwt.authentication import JWTAuth

from .models import CustomUser
from .schema import UserSchema

router = Router()


@router.post("/", response=UserSchema)
def create(request: WSGIRequest, payload: UserSchema) -> UserSchema:  # noqa
    """Create a new user."""
    user = CustomUser.objects.create_user(
        **payload.dict(exclude_unset=True, exclude_none=True),
    )
    return UserSchema.from_orm(user)


@router.get("/", response=UserSchema, auth=JWTAuth())
def get_user(request) -> UserSchema:  # noqa
    """Get user details."""
    user: CustomUser = request.auth

    return UserSchema.from_orm(user)
