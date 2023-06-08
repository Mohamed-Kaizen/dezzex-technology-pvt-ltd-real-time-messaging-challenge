"""API routes for users app."""
from django.core.handlers.wsgi import WSGIRequest
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken

from .models import CustomUser
from .schema import UserSchema

router = Router()


@router.post("/")
def create(request: WSGIRequest, payload: UserSchema) -> dict[str, str]:  # noqa
    """Create a new user."""
    user = CustomUser.objects.create_user(
        **payload.dict(exclude_unset=True, exclude_none=True),
    )

    refresh = RefreshToken.for_user(user)

    return {
        "user": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@router.get("/", auth=JWTAuth())
def get_user(request) -> dict:  # noqa
    """Get user details."""
    user: CustomUser = request.auth

    return {
        "user": user.username,
        "email": user.email,
        "full_name": user.full_name,
    }
