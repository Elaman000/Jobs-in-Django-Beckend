from rest_framework import serializers
from .models import *
from customuser.models import CustomUser



class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = ("__all__")



