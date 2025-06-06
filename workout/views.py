import collections
import logging

from django.contrib.auth.models import User
from django.core.mail import mail_managers
from django.db import transaction
from django.db.models import Count, Sum, Q
from django.http import Http404
from django.utils import timezone
from rest_framework import serializers, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
# from wkhtmltopdf.views import PDFTemplateView
from rest_framework import permissions, authentication
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import time
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# from django.conf.urls import include, url
from django.urls import re_path as url

from workout.models import UserProfile
from rest_framework.pagination import PageNumberPagination
from workout.serializers import (UserProfileSerializer, OtpVerificationSerializer,UserProfileListSerializer,
ExcerciseslistSerializer)
import random
from common_function.send_otp_mail import send_otp_via_email
from common_function.permission_decorator import IsSuperUser
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from common_function.send_otp_mail import send_otp_via_email
from workout.models import Excerciseslist
from rest_framework import status

@api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# @authentication_classes((TokenAuthentication,))
@authentication_classes([])
@permission_classes([])
def user_profile_register(request):
    """
    {
    userData: [
        {
        user: {
            first_name: "Pooja",
            last_name: "pal",
            email: "poojapal11151@gmail.com",
        },
        username: "poojapal11151@gmail.com",
        email: "poojapal11151@gmail.com",
        phone: "+917654897654",
        is_active: true,
        from_to: "2023-01-31",
        valid_to: "2023-10-28",
        role_type: "Super User",
        userid: "4",
        },
    ],
    file: [<TemporaryUploadedFile: IMG_20210321_153801.jpg (image/jpeg)>],
    };
    """
    # if this is a POST request we need to process the form data


    # create a form instance and populate it with data from the request:
    data = dict(request.data)
    updatedData = json.loads(data['userData'][0])
    id_ = int(updatedData['userid'])
    if (id_ <= 0):
        data = updatedData.copy()
        if request.FILES:
            convertDictToObj = dict(request.FILES)
            data['pic'] =  convertDictToObj['file'][0]
        role = data.pop('role_type')
        active = data.pop('is_active')
        data['user']['username'] = data.get('email')

        # pic = data['pic']
        user_pref_form = UserProfileSerializer(
            data=data, context={'request': request, })

        # user_pref_form.pic = pic.url

        user_profile_valid = False
        user_profile_valid = user_pref_form.is_valid()

        if user_profile_valid:
            user_profile = None
            username = None
            email = None
            with transaction.atomic():
                email = updatedData.get('email',None)

                # save user profile ***********************
                user_profile = user_pref_form.save()
                user = User.objects.get(id=user_profile.user.id)

                if (role == 'Super User'):
                    user.is_superuser = True
                    user.is_staff = True
                else:
                    user.is_superuser = False
                    user.is_staff = False
                if active:
                    user.is_active = True
                else:
                    user.is_active = False
                user.save()
                try:
                    send_otp_via_email(data['email'])
                except Exception as e:
                    print(e, "send otp via email")
                print("user is created successfully")
                # BY PASS SAVE
                # user_profile = user_pref_form



            return Response(user_pref_form.data, status=status.HTTP_201_CREATED)

        else:
            pass
            print(user_pref_form.errors)

        return Response(user_pref_form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        user_detail = User.objects.get(id=id_)
        userprofile_detail = UserProfile.objects.get(user_id=id_)

        user_detail.first_name = updatedData['user']['first_name']
        user_detail.last_name = updatedData['user']['last_name']

        if updatedData['is_active']:
            user_detail.is_active = True
        else:
            user_detail.is_active = False

        if (updatedData['role_type'] == 'Super User'):
            user_detail.is_superuser = True
            user_detail.is_staff = True
        else:
            user_detail.is_superuser = False
            user_detail.is_staff = False
        user_detail.save()

        userprofile_detail.phone = updatedData['phone']
        userprofile_detail.from_to = updatedData['from_to']
        userprofile_detail.valid_to = updatedData['valid_to']
        if request.FILES:
            convertDictToObj = dict(request.FILES)
            userprofile_detail.pic = convertDictToObj['file'][0]
        userprofile_detail.save()
        #  # 'pic' : base_url+userprofile_detail.pic.url
        response_data = {'user' : updatedData['user']['first_name']}
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def verify_otp(request):
    """
    {
    "email" : "balaprajapati02@gmail.com",
    "otp" : ""
    }
    """
    if request.method == 'POST':
        time.sleep(2)
        try:
            data = request.data
            serializer = OtpVerificationSerializer(data = data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                try:
                    user = UserProfile.objects.get(email = email)

                    if (user.otp != otp):
                        response_ = {
                                        'status' : 400,
                                        'message' : 'something went wrong',
                                        'data' : 'invalid otp'
                                        }
                        return Response(response_)
                    user.is_verified = True
                    user.save()
                    response_ = {
                                    'status' : 200,
                                    'message' : 'account is verified',
                                    'data' : 'account is verified'
                                    }
                    return Response(response_)

                except Exception as e:
                    print(e)
                    response_ = {
                                'status' : 400,
                                'message' : 'something went wrong',
                                'data' : 'invalid email'
                                }
                    return Response(response_)

            response_ = {'status' : 400,
                        'message' : 'something went wrong',
                        'data' : serializer.errors
                        }
            return Response(response_)



        except Exception as e:
            print(e)
            return Response({"status" : 400,
                            "message" : 'something went wrong'})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def resend_otp(request):
    """
    {
    "email" : "balaprajapati02@gmail.com",
    }
    """    
    if request.method == 'POST':
        data = request.data
        try:
            send_otp_via_email(data['email'])
        except Exception as e:
            print(e, "send otp via email")
            return Response({"status" : 500,
                            "message" : 'something went wrong'})
        print("otp resend successfully")
        return Response({"status" : 200,
                            "message" : 'otp resend successfully'})



from django.core.exceptions import PermissionDenied

@csrf_exempt
@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def login_user(request):
    """
{"Email_Address":"bala@gmail.com","password":"1234"}
{"username":"phone no.","password":"1234"}
    """
    reqBody = request.data
    data = {}
    # reqBody = json.loads(request.body)
    username = reqBody['username']
    password = reqBody['password']
    try:

        username = User.objects.get(email=username.lower()).username
        checkpermission = User.objects.get(email=username)
        userprofile = UserProfile.objects.get(user=checkpermission)

        # check weather user is active
        if not checkpermission.is_active:
            validation_error = "Account not active"
            return Response(validation_error, status=status.HTTP_403_FORBIDDEN)

        # custome user profile is varified field validation
        if not userprofile.is_verified:
            validation_error = "Account is not verified"
            return Response(validation_error, status=status.HTTP_401_UNAUTHORIZED)

        # check weather user have permission or not
        if not checkpermission.is_superuser or not checkpermission.is_staff:
            validation_error = "User is not superuser"
            return Response(validation_error, status=status.HTTP_403_FORBIDDEN)
            # raise PermissionDenied
        # if not checkpermission.is_staff:
        #     print("user is not super user")
        #     validation_error = "User is not superuser"
        #     return Response(validation_error, status=status.HTTP_403_FORBIDDEN)
            
        Account = authenticate(username=username, password=password)

    except Exception as e:

        validation_error = "Incorrect Login credentials"
        return Response(validation_error, status=status.HTTP_400_BAD_REQUEST)

    if Account != None:
        token = Token.objects.get_or_create(user=Account)[0].key
        login(request, Account)
        data["message"] = "user logged in"
        data["email_address"] = Account.email
        data['token'] = token
        data['username'] = Account.username
        Res = data
        return Response(Res, status=200)

    else:
        validation_error = "Incorrect Login credentials"
        return Response(validation_error, status=400)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == "POST":
        try:

            request.user.auth_token.delete()
            logout(request)

            return Response("logout user successfully")

        except Exception as e:
            print("having issue ", e)
            pass
    else:
        return Response('Pass user authentication details')

@api_view(['GET','POST'])
@authentication_classes([])
@permission_classes([])
def userprofile_list(request):
    # {"limit" : 100}
    data = request.data
    user = UserProfile.objects.all()
    paginator = PageNumberPagination()
    if data:
        limit = int(data['limit'])
        paginator.page_size = limit
    else:
        paginator.page_size = 1

    result_page = paginator.paginate_queryset(user, request)

    serializer = UserProfileListSerializer(
        result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([])
def user_filter(request):
    """
    {
    "value" : "r"
    }
    """
    model = UserProfile
    filter_data =[]
    if request.method == 'POST':
        if request.data:
            data = request.data
            result_data = model.objects.filter(Q(user__username__contains=data['value']) | Q(email__contains=data['value']) | Q(phone__contains=data['value']))
            paginator = PageNumberPagination()
            paginator.page_size = 1
            if data:
                if data['limit']:
                    
                    limit = int(data['limit'])
                    paginator.page_size = limit
            else:
                paginator.page_size = 1
            if result_data:
                result_page = paginator.paginate_queryset(result_data, request)
                serializer = UserProfileListSerializer(
                    result_page, context={'request': request, }, many=True)
                return paginator.get_paginated_response(serializer.data)

            else:
                result_page = paginator.paginate_queryset(result_data, request)
                serializer = UserProfileListSerializer(
                    result_page, context={'request': request, }, many=True)

                return paginator.get_paginated_response(serializer.data)

    elif request.method == 'GET':
        return Response('Enter Some Value')


 # u.is_active and u.is_superuser

from datetime import date
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([])
def FiterPastDate(request):
    users = UserProfile.objects.all()
    today = date.today()
    data = {"Today Data is " : today}
    for user in users:
        if (user.valid_to):
            if (user.valid_to < today):
                User.objects.filter(pk=user.user.id).update(is_active=False)
            pass
        pass
    return Response(data)


# get user by token
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([])
def get_user_by_token(request):
    """
    {
    "token": "54sd45432131303213265461623232322"
    }
    """
    base_url =  "{0}://{1}".format(request.scheme, request.get_host())
    if request.method == "GET":
        # abc = User.objects.all()
        # for i in abc:
        #     print(i.id, i.username, "users id and username ")
        data = 'enter some value'
        # base_url =  "{0}://{1}/".format(request.scheme, request.get_host())
        return Response(data)

    elif request.method == "POST":
        fetch_data = request.data
        data = {}
        try:
            token = Token.objects.get(key=fetch_data['token'])
            user_detail = User.objects.get(id=token.user_id)
            user_profile = UserProfile.objects.get(email=user_detail.email)

            current_user_id = user_profile.user.id

            if user_profile.user.username:
                username = user_profile.user.username
            else:
                username = ""

            if user_profile.pic:
                picture = base_url+user_profile.pic.url
            else:
                picture = None

            if user_profile.user.first_name:
                first_name = user_profile.user.first_name
            else:
                first_name = ""

            if user_profile.user.last_name:
                last_name = user_profile.user.last_name
            else:
                last_name = ""

            if user_profile.email:
                email = user_profile.email
            else:
                email = ""

            if user_profile.phone:
                phone = str(user_profile.phone)
            else:
                phone = ""

            if user_profile.from_to:
                from_to = user_profile.from_to
            else:
                from_to = ""

            if user_profile.valid_to:
                valid_to = user_profile.valid_to
            else:
                valid_to = ""

            if user_profile.user.is_superuser and user_profile.user.is_staff:
                role_type = 'Super User'
            else:
                role_type = ''



            if token:
                IsAuthenticate = True
            else:
                IsAuthenticate = False

            # data = {"username" : user_profile.user}
            user_details = {'username' : username,
                     "picture" : picture, "first_name" : first_name, "last_name" : last_name,
                     "email" : email, "phone" : phone, 'role_type' : role_type,
                    "id": current_user_id, "IsAuthenticate" : IsAuthenticate, 'from_to' : from_to, 'valid_to' : valid_to  }
            data.update(user_details)
            return Response(data)
        except Exception as e:
            data = 'Invalid Token'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


# @is_superuser
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
@authentication_classes((TokenAuthentication,))
def get_user_id(request):
    """
    {"userid" : "9"}
    """

    user_data = {}
    base_url =  "{0}://{1}".format(request.scheme, request.get_host())
    if request.method == "GET":

        print(request.data , "comming from user detail api")
    if request.method == "POST":
        u_id = request.data
        try:
            # user_detail = User.objects.get(id=u_id["userid"])
            user_profile = UserProfile.objects.get(user_id=u_id["userid"])
        except ObjectDoesNotExist:
            error = "user not found"
            return Response(error)

        current_user_id = user_profile.user.id

        if user_profile.user.username:
            username = user_profile.user.username
        else:
            username = ""

        if user_profile.pic:
            picture = base_url+user_profile.pic.url
        else:
            picture = None

        if user_profile.user.first_name:
            first_name = user_profile.user.first_name
        else:
            first_name = ""

        if user_profile.user.last_name:
            last_name = user_profile.user.last_name
        else:
            last_name = ""

        if user_profile.email:
            email = user_profile.email
        else:
            email = ""

        if user_profile.phone:
            phone = str(user_profile.phone)
        else:
            phone = ""

        if user_profile.valid_to:
            valid_to = str(user_profile.valid_to)
        else:
            valid_to = ""

        if user_profile.from_to:
            from_to = str(user_profile.from_to)
        else:
            from_to = ""

        if user_profile.user.is_active:
            check_active =  user_profile.user.is_active
        check_active =  user_profile.user.is_active


        if user_profile.user.is_superuser:
            role_type = 'Super User'
        else:
            role_type = 'Customer'

        user_details = {'username' : username,
                 "picture" : picture, "first_name" : first_name, "last_name" : last_name,
                 "email" : email, "phone" : phone, "from_to" : from_to, "valid_to" : valid_to,
                 'active' : check_active, "id": current_user_id, "role_type" : role_type}
        user_data.update(user_details)
        return Response(user_data)

    return Response(user_data)


import json
# Fetch data through API
@api_view(['GET', 'POST'])
@permission_classes([])
@authentication_classes([])
def getExcercise(request):
    """ if you want with limit data then you should pass

    {"limit" : 100}"""
    # Excerciseslist = []
    # data = Excerciseslist.objects.all()
    # for ex in data:
    #     data = {'bodyPart' : ex.bodypart, 'equipment' : ex.equipment, 'gifUrl' : ex.gif_url, 'id' : ex.id, 'name' : ex.name, 'target' : ex.target}
    #     Excerciseslist.append(data)
    # return Response(Excerciseslist)


    data = request.data
    excercise = Excerciseslist.objects.all()
    paginator = PageNumberPagination()
    if data:
        limit = data['limit']
        paginator.page_size = limit
    else:
        paginator.page_size = 10

    result_page = paginator.paginate_queryset(excercise, request)
    serializer = ExcerciseslistSerializer(
        result_page, many=True)

    return paginator.get_paginated_response(serializer.data)


# calculate BMI
# [weight (kg) / height (cm) / height (cm)] x 10,
@api_view(['GET', 'POST'])
@permission_classes([])
@authentication_classes([])
def calculteByKey(request):
    """Calculate BMI height=cm and weight=kg
    {"bmi" : {"height": 10, "weight" : 20}}
    
    Calculate Weight loass weight=kg and goal_weight=kg
    {"cal_weight_loss" : {"current_weight": 100, "goal_weight" : 60}}
    """
    data = request.data
    

    if data:
        filterByKey = list(data.keys())[0]
        if filterByKey == 'bmi':
            height = data['bmi']['height']
            weight = data['bmi']['weight']
            calculate = round(((weight/height/height)*10000),1)
            data = {'BMI' : calculate}
        elif filterByKey == 'cal_weight_loss':
            #  progress of weight loss based on a given current weight and goal weight 
            # progress = (200 - 150) / 150 = 0.33 or 33%
            weight = data['cal_weight_loss']['current_weight']
            goalWeight = data['cal_weight_loss']['goal_weight']
            progress = round((weight - goalWeight) * 100 / goalWeight,2)
            data = {'PROGRESS_WEIGHT_LOSS' : progress }
    else:
        data ={'calulate' : 'BMI, Body Fate'}
    return Response(data)


