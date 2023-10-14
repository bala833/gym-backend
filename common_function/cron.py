# from datetime import date
# from workout.models import UserProfile

# def deactivate_job():
#     users = UserProfile.objects.all()
#     today = date.today()
#     print("Today date is: ", today)
#     data = {"Today Data is " : today}
#     for user in users:
#         if (user.valid_to):
#             if (user.valid_to < today):
#                 User.objects.filter(pk=user.user.id).update(is_active=False)
#                 print(f"user are going to expire :{user.user.username}" )


def printbala_job():
	 print('balaaaaaaaaaaaa')


printbala_job()

from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours
    RETRY_AFTER_FAILURE_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    # code = 'gym_backend.cron.deactivate_job'    # a unique code
    code = 'printbala_job'    # a unique code

    def do(self):
        # code()