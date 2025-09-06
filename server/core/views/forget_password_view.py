import logging as loggers
from datetime import date
from django.conf import settings
from rest_framework import status
from django.db import transaction
from core.threads import send_mail
from rest_framework import permissions
from core.models import ForgetPassword
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from core.utils.reset_email_token_util import reset_email_token


User = get_user_model()
loggers.basicConfig(level=loggers.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = loggers.getLogger(__name__)


class ForgetPasswordView(APIView):

    permission_classes = (permissions.AllowAny,)

    @transaction.atomic
    def post(self, request):
        try:
            email = request.data.get('email', '')
            otp = request.data.get('otp', True)

            if email is None or email == '':
                message = {'detail': 'Email is required to reset password'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            user = get_object_or_404(User, email=email)
            token_exists = ForgetPassword.objects.filter(user=user)
            token_exists.delete()
            current_reset_token = reset_email_token(50, otp)
            token = ForgetPassword.objects.create(
                user=user, reset_email_token=current_reset_token)
            key = {
                'username': user.username,
                'button': settings.REACT_DOMAIN+'auth/reset-password/'+str(token.reset_email_token),
                'year': date.today().year
            }
            if otp:
                key.update({'otp': current_reset_token, 'button': None})
            send_mail(subject="Reset Your Password", html_content="auth/forgetPassword.html",
                      recipient_list=[email], key=key)
            return Response({'detail': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("%d", e)
            return Response({'detail': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
