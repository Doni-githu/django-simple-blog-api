from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'name', 'email', 'password', 'username', 'email_verify']
        extra_kwargs = {    
            'password': {'write_only': True},
            "email_verify": {'read_only': True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            
        instance.save()
        return instance
    
class EmailConfirm(serializers.Serializer):
    code = serializers.CharField()