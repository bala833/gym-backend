from django.apps import AppConfig
from common_function import userDeactiveJob 

class WorkoutConfig(AppConfig):
    name = 'workout'

    # def ready(self):
    #     # from common_function.jobs import userDeactiveJob
    #     userDeactiveJob.start()
