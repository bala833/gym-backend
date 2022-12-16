# from django.conf.urls import url
from django.urls import include, path
from django.urls import re_path as url

from rest_framework.authtoken.views import obtain_auth_token


from workout.views import  (
                login_user,user_profile_register,verify_otp,user_logout, userprofile_list,user_filter,
                FiterPastDate, get_user_by_token, get_user_id, 
                getExcercise,calculteByKey
               )
urlpatterns = [
    url(r'^userprofile/register/$', user_profile_register, name='user-register'),
    url(r'^verify/$', verify_otp, name='verify-otp'),
    url(r'^login-user/$', login_user, name='login-user'),
    url(r'^logout-user/$', user_logout, name='logout-user'),
    url(r'^user-list/$', userprofile_list, name='user-list'),
    url(r'^user-filter/$', user_filter, name='user-filter'),
    url(r'^getuser-id/$', get_user_id, name='get-user-id'),
    url(r'^datefilter/$', FiterPastDate, name='datefilter'),
    url(r'^get-user-token/$', get_user_by_token, name='get-user-by-token'),
    url(r'^excercise/$', getExcercise, name='Excerciseslist'),
    url(r'^calculatebykey/$', calculteByKey, name='calculatebykey'),




]


# once super user create client then client will get reset password link on his/her mail that will valid for 
# some time.

# when super user or client is going to login he will get otp then only he can login.
