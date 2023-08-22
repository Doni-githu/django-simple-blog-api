from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer, EmailConfirm
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt, datetime
from rest_framework.mixins import status
from src.utils import send_email, generate_verification_code, decode_verification_code


class RegisterView(APIView):
    def post(self, request):
        if request.COOKIES.get("jwt"):
            raise AuthenticationFailed(
                code=403, detail="You have already authenticated"
            )

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        payload = {
            "id": serializer.data.get("id"),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload=payload, key="awdawdwad", algorithm="HS256")
        res = Response()
        res.data = {
            "user": serializer.data.get("id"),
        }
        res.status_code = status.HTTP_201_CREATED
        send_email(
            "Verify code",
            [serializer.data.get("email")],
            f"It's your code {generate_verification_code(serializer.data.get('id'))}",
        )
        return res


class SendVerifyCode(APIView):
    def post(request, id):
        user = User.objects.get(id=id)

        serializeredData = EmailConfirm(data=request.data)
        serializeredData.is_valid(raise_exception=True)
        code = serializeredData.data.get("code")
        if code != generate_verification_code(id):
            raise AuthenticationFailed(
                detail="Code is incorreted\nPlease Try again", code=403
            )
        serializeredUser = UserSerializer(user)
        res = Response()
        payload = {
            "id": serializeredUser.data.get("id"),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow(),
        }
        token = jwt.encode(payload=payload, key="awdawdwad", algorithm="HS256")
        res.set_cookie(key="jwt", value=token, httponly=True)
        res.data = {"user": serializeredUser.data, "token": token}
        return res


class LoginView(APIView):
    def post(self, request):
        if request.COOKIES.get("jwt"):
            raise AuthenticationFailed(
                code=403, detail="You have already authenticated"
            )

        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed(code=404, detail="User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed(code=403, detail="Incorrect password!")

        if user.email_verify == False:
            send_email(
                "Verify code",
                [email],
                f"Your verify code is {generate_verification_code(user.pk)}",
            )
            return Response(
                {"detail": "Your are not confirm your email please confirm"},
                status=status.HTTP_403_FORBIDDEN,
            )

        payload = {
            "id": user.pk,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload=payload, key="awdawdwad", algorithm="HS256")
        serializer = UserSerializer(user)
        res = Response()
        res.set_cookie(key="jwt", value=token, httponly=True)

        res.data = {"token": token, "user": serializer.data}
        return res


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        if token is None:
            raise AuthenticationFailed(code=404, detail="Unauthenticated!")

        try:
            payload = jwt.decode(token, "awdawdwad", algorithms="HS256")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(code=404, detail="Unauthenticated!")
        user = User.objects.get(id=payload["id"])

        if user.email_verify == False:
            send_email(
                "Verify code",
                user.email,
                f"Your verify code is {generate_verification_code(user.pk)}",
            )
            raise AuthenticationFailed(
                detail="You aren't confirm your email pleas go to your email"
            )

        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        res = Response()
        if not request.COOKIES.get("jwt"):
            raise AuthenticationFailed(code=403, detail="Unauthenticated!")
        res.delete_cookie("jwt")
        res.data = {"message": "success log out"}

        return res
