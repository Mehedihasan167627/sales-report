from rest_framework import serializers 
from .models import User
from django.contrib.auth.hashers import make_password

class CreateUserSerializer(serializers.ModelSerializer):
    retype_password=serializers.CharField()
    class Meta:
        model=User 
        fields=["full_name","email","password","retype_password"]

    def validate(self, attrs):
        retype_password=attrs.pop("retype_password")
        password=attrs["password"]

        if password!=retype_password:
            raise serializers.ValidationError("Doesn't match your confirm password")
        attrs["password"]=make_password(password)
        return super().validate(attrs)
    
    