from rest_framework import serializers, generics, status
from workout.models import UserProfile,Excerciseslist
import django.contrib.auth.password_validation as validators
import base64

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed


from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets



class CreateUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name','password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        username = data.get('username')
        if username:
            try:
                User.objects.get(username=username)
                raise serializers.ValidationError(
                    "This Mobile Phone Number has been already registered.")
            except User.DoesNotExist:
                pass
        email = data.get('email')
        if email:
            try:
                User.objects.get(email=email)
                raise serializers.ValidationError(
                    "This Email has been already registered.")
            except User.DoesNotExist:
                pass

        user = User(**data)

        # get the password from the data
        password = data.get('password')

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=User)

        # the exception raised here is different than serializers.ValidationError
        except serializers.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        # return data
        return super(CreateUserSerializer, self).validate(data)


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    user = CreateUserSerializer()
    class Meta:
        model = UserProfile
        fields = (
            'email',
            'phone',
            'user',
            'pic',
            'otp',
            'valid_to',
            'from_to',
        )
        # bad idea. shd be using fields ...
        # exclude = ('user', 'activation_key', 'key_expires',)

    def create(self, validated_data):
        # print "in create", validated_data
        user_data = validated_data.pop('user')
        user = User(
            email=user_data['email'],
            username=user_data['username'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        user.set_password(user_data['password'])
        # user email verification disabled for now **************
        # user.is_active = True
        # role = validated_data.get('role_type') 

        # if not role:
        #     raise serializers.ValidationError('Role type is requried !')    

        # elif (role == 'Super User'):
        #     user.is_superuser = True
        #     user.is_staff = True

        # else:
        #     pass
        user.save()

        user_profile = UserProfile.objects.create(user=user, **validated_data)

        return user_profile

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('This is a required field !')

        else:
            try:
                UserProfile.objects.get(email=value)
                raise serializers.ValidationError('There is already a user registered with this email id !')

            except UserProfile.MultipleObjectsReturned:
                raise serializers.ValidationError('There is already a user registered with this email id !')

            except UserProfile.DoesNotExist:
                pass
                # return email

        return value

    def validate_phone(self, value):
        if value:
            try:
                UserProfile.objects.get(phone=value)
                raise serializers.ValidationError(
                    "This Mobile Phone Number has been already registered.")

            except UserProfile.MultipleObjectsReturned:
                raise serializers.ValidationError('This Mobile Phone Number has been already registered.')

            except UserProfile.DoesNotExist:
                pass
        else:
            raise serializers.ValidationError('This is a required field !')


        return value

    def validate_pic(self, value):
        if value:
            pass
        else:
            pass
            
        return value




class OtpVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()



class UserProfileFromSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        userImg = UserProfile.objects.get(user_id = obj.user.id)
        return {'id' : obj.user.id, 'username' : obj.user.username, 'is_active' : obj.user.is_active, 'is_superuser' : obj.user.is_superuser, 'image' : userImg.pic}
    class Meta:
        model = UserProfile
        fields = ('id','email','phone','pic','user','otp','is_verified')


class UserProfileListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {'id' : obj.user.id, 'username' : obj.user.username, 'is_active' : obj.user.is_active, 'is_superuser' : obj.user.is_superuser}
    class Meta:
        model = UserProfile
        fields = ('id','email','phone','pic','user','otp','is_verified')

    # def validate_user(self, value):
    #     if value:
    #         return_data = User.objects.get(id=value)
    #         print(return_data,"ddddddddddddddddddddddddddd")

    #     return return_data


# class ProductAttributeSerializer(serializers.ModelSerializer):
#     """
#     serializer for productAttribute
#     """

#     attribute_title = serializers.SerializerMethodField()

#     # attribute = AttributeOptionSerializer()

#     def get_attribute_title(self, obj):
#         return obj.attribute.title

#     class Meta:
#         model = ProductAttribute
#         fields = ('attribute_title', 'value')


class ExcerciseslistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Excerciseslist
        fields = ('id', 'bodypart','equipment','gif_url','image','name','target')
