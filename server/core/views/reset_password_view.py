from rest_framework import status
from core.models import ForgetPassword
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta, timezone

User = get_user_model()


class ResetPasswordAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Parameters:
            email
            password
            otp
        """
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        otp = request.data.get('otp', '')
        if email and password and otp:
            user = get_object_or_404(User, email=email)

            token = get_object_or_404(ForgetPassword, user=user)

            if (token.created_at+timedelta(minutes=15)).replace(tzinfo=timezone.utc) < datetime.now(timezone.utc) - timedelta(minutes=15):

                token.activated = False
                token.is_expired = True
                token.save()
                return Response({"message": "OTP expired", "status": "400"}, status=status.HTTP_400_BAD_REQUEST)

            if token.reset_email_token == otp and token.activated and not token.is_expired:
                user.set_password(password)
                user.save()
                token.delete()
                return Response({"message": "Password reset successfully", "status": "200"}, status=status.HTTP_200_OK)
            return Response({"message": "Invalid OTP Regenerate OTP", "status": "400"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Email, Password and OTP are required", "status": "400"}, status=status.HTTP_400_BAD_REQUEST)
