from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken

def create_token(user):
    refresh = RefreshToken.for_user(user)

    # Access the token directly
    access_token = refresh.access_token

    # Manually set the expiration time for the access token
    custom_lifetime = timedelta(days=180)
    access_token.set_exp(lifetime=custom_lifetime)

    # Explicitly include user ID
    access_token['user_id'] = user.id

    return {
        'refresh': str(refresh),
        'access': str(access_token),
    }
