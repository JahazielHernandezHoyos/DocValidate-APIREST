from functools import wraps
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework.response import Response
from rest_framework import status


def jwt_required(view_func):
    """
    Decorator that checks if a valid JWT token is present in the request.
    If the token is valid and of type "access", the view function is called.
    Otherwise, a 401 Unauthorized response is returned.

    Args:
        view_func (function): The view function to be decorated.

    Returns:
        function: The decorated view function.
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        try:
            token = UntypedToken(request.auth)
            if not token["token_type"] == "access":
                raise InvalidToken("Invalid token type")
        except InvalidToken:
            return Response(
                {"detail": "Invalid or missing token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return view_func(request, *args, **kwargs)

    return wrapped_view
