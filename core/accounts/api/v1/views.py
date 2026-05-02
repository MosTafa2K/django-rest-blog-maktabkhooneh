from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import (
    GenericAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.api.utils import SendEmailAsThread
from accounts.models import Profile

from .serializers import (
    ChangePasswordSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ProfileSerializer,
    RegisterSerializer,
)

User = get_user_model()


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "user_id": user.pk,
                "email": user.email,
                "token": token.key,
            }
        )


class CustomDestroyAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ChangePasswordAPIView(GenericAPIView):
    model = User
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(
                serializer.validated_data.get("old_password")
            ):
                return Response(
                    {"old_password": "Password is wrong."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.validated_data.get("new_password"))
            self.object.save()
            return Response(
                {
                    "result": "success",
                    "detail": "Password has been changed!",
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        qs = self.get_queryset()
        obj = get_object_or_404(qs, user=self.request.user)
        return obj


class TestSendEmail(APIView):
    def post(self, request, *args, **kwargs):
        mail = EmailMessage(
            "email/hello.tpl",
            {"name": "Mostafa"},
            "from@admin.com",
            to=["m2kappswindows81@gmail.com"],
        )
        email_thread = SendEmailAsThread(mail)
        email_thread.start()
        return Response({"detail": "Email has been sent. Please check your inbox!"})
