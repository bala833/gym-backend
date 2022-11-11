from django.db import models
from django_extensions.db.models import (TimeStampedModel,
                                         TitleDescriptionModel)
class RazorpayPayment(TimeStampedModel):
	amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=False, null=False)
	name = models.CharField(max_length=255, blank=False, null=False)
	provider_order_id = models.CharField(max_length=255, blank=False, null=False)
    # user = models.OneToOneField(User, on_delete=models.PROTECT)

