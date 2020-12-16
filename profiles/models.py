import uuid
from django.db import models
from user.models import User

class UserProfile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, unique=False)
    last_name = models.CharField(max_length=50, unique=False)
    phone_number = models.IntegerField(null=False, blank=False)
    area_code = models.CharField(max_length=10, null=False, blank=False)
    country_code = models.CharField(max_length=10, null=False, blank=False)
    

    class Meta:
        '''
        set table name in db
        '''
        db_table = "profile"
