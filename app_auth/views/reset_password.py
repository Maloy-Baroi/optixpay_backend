from multiprocessing import Process

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random

from app_auth.models import CustomUser, UserVerificationToken
from services.send_main import send_verification_email
from utils.common_response import CommonResponse


class SendOTPView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            if email:
                user = CustomUser.objects.filter(email=email).first()
                if user:
                    # Generate OTP
                    otp = random.randint(100000, 999999)
                    # Store OTP in a way you can validate it later; here it's simplified
                    if not user:
                        return CommonResponse("error", {"message": "No user found with this email!"},
                                              status_code=status.HTTP_400_BAD_REQUEST)

                    otp_cached = UserVerificationToken.objects.get(user=user)

                    if otp_cached is None:
                        return CommonResponse("error", {"message": "No User found with this email"},
                                              status_code=status.HTTP_400_BAD_REQUEST)

                    otp = random.randint(1000, 9999)

                    otp_cached.token = otp
                    otp_cached.save()

                    # Send OTP by email
                    # send_mail(
                    #     'Your Password Reset OTP',
                    #     f'Your OTP is: {otp}',
                    #     settings.DEFAULT_FROM_EMAIL,
                    #     [email],
                    #     fail_silently=False,
                    # )
                    # Start a new process for sending email
                    email_process = Process(target=send_verification_email, args=(user.email, otp))
                    email_process.start()
                    return CommonResponse("success", {'message': 'OTP sent to email'}, status_code=status.HTTP_200_OK)
                return CommonResponse("error", {'error': 'User with this email does not exist'},
                                      status_code=status.HTTP_404_NOT_FOUND)
            return CommonResponse("error", {'error': 'Email field is required'},
                                  status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return CommonResponse("error", {'error': str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            otp = request.data.get('otp')
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')

            if new_password != confirm_password:
                return CommonResponse("error", {'error': 'Passwords do not match'},
                                      status_code=status.HTTP_400_BAD_REQUEST)

            if email and otp and new_password:
                user = CustomUser.objects.get(email=email)

                otp_cached = UserVerificationToken.objects.get(user=user)
                if user and int(otp) == otp_cached.token:  # Validate OTP
                    # Reset password
                    user.set_password(new_password)
                    user.profile.otp = None  # Clear the OTP
                    user.save()
                    user.profile.save()
                    return CommonResponse("success", {'message': 'Password has been reset successfully'},
                                          status_code=status.HTTP_200_OK)
                return CommonResponse("error", {'error': 'Invalid OTP or email'},
                                      status_code=status.HTTP_400_BAD_REQUEST)
            return CommonResponse("error", {'error': 'All fields are required'},
                                  status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return CommonResponse("error", {'error': str(e)}, status_code=status.HTTP_400_BAD_REQUEST)
