from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken

def create_token(user):
    refresh = RefreshToken.for_user(user)

    # Access the token directly
    access_token = refresh.access_token

    # Manually set the expiration time for the access token
    custom_lifetime = timedelta(days=1000)
    access_token.set_exp(lifetime=custom_lifetime)

    # Explicitly include user ID
    access_token['user_id'] = user.id
    mobile_auth_url = f"/api/v1/app-sms/regenerate-token/{str(access_token)}"

    return {
        'mobile_auth_url': mobile_auth_url
    }
