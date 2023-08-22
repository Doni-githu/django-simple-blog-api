from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt, datetime

class RegisterView(APIView):
    def post(self, request):
        if request.COOKIES.get('jwt'):
            raise AuthenticationFailed(code=403, detail='You have already authenticated')
                    
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        payload = {
            'id': serializer.data.get('id'),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        
        token =  jwt.encode(payload=payload, key='awdawdwad', algorithm='HS256')
        res = Response()
        res.set_cookie(key='jwt', value=token, httponly=True)
        res.data = {
            'user': serializer.data,
            'token': token
        }
        
        return res


class LoginView(APIView):
    def post(self, request):
        if request.COOKIES.get('jwt'):
            raise AuthenticationFailed(code=403, detail='You have already authenticated')
        
        
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        
        
        if user is None:
            raise AuthenticationFailed(code=404, detail='User not found!')
        
        
        if not user.check_password(password):
            raise AuthenticationFailed(code=403, detail='Incorrect password!')
        
        payload = {
            'id': user.pk,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload=payload, key='awdawdwad', algorithm='HS256')
        serializer = UserSerializer(user)
        res = Response()
        res.set_cookie(key='jwt', value=token, httponly=True)
        
        res.data = {
            'token': token,
            'user': serializer.data
        }
        return res
    
    
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if token is None:
            raise AuthenticationFailed(code=404, detail='Unauthenticated!') 
        
        try:
            payload = jwt.decode(token, 'awdawdwad', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(code=404, detail='Unauthenticated!') 
        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        res = Response()
        if not request.COOKIES.get('jwt'):
            raise AuthenticationFailed(code=403, detail='Unauthenticated!')
        res.delete_cookie('jwt')
        res.data = {
            "message": "success log out"
        }
        
        return res