# import time


# date1 = "01/01/2016"
# date2 = "01/01/2016"

# d1 = time.strptime(date1, "%d/%m/%Y")
# d2 = time.strptime(date2, "%d/%m/%Y")

# print(d1 < d2)

from workout.models import UserProfile


def FiterPastDate():
	users = UserProfile.objects.all()
	for user in users:
		print(user.id, user.valid_to)



def run():
	FiterPastDate()