from rest_framework import serializers
from .models import Department, Job, Hiredemployee

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class HiredemployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hiredemployee
        fields = '__all__'
