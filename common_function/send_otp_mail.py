from django.core.mail import send_mail
import random
from django.conf import settings
from workout.models import UserProfile



def send_otp_via_email(email):
	subject = 'Your account verification email'
	otp = random.randint(10000, 999999)
	message = f'Your otp is {otp} '
	email_from = settings.EMAIL_HOST_USER
	send_mail(subject, message, email_from, [email])
	user_obj = UserProfile.objects.get(email = email)
	user_obj.otp = otp
	user_obj.save()
