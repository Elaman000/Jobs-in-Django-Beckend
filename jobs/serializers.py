from rest_framework import serializers
from .models import *
from customuser.models import CustomUser



class JobsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    title_info = serializers.CharField(max_length=250)
    published = serializers.BooleanField(default=True)
    wage = serializers.IntegerField()
    number_persons=serializers.IntegerField()
    city = serializers.SlugRelatedField(queryset=City.objects.all(), slug_field='id')
    area = serializers.SlugRelatedField(queryset=Area.objects.all(), slug_field='id')
    user = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username')

    def create(self, validate_data):
        return Jobs.objects.create(**validate_data)


    def update(self, instance, validated_data):
        # Обновляем поля объекта `instance` новыми данными
        instance.title = validated_data.get('title', instance.title)
        instance.title_info = validated_data.get('title_info', instance.title_info)
        instance.published = validated_data.get('published', instance.published)
        instance.wage = validated_data.get('wage', instance.wage)
        instance.number_persons = validated_data.get('number_persons', instance.number_persons)
        instance.city = validated_data.get('city', instance.city)
        instance.area = validated_data.get('area', instance.area)
        instance.user = validated_data.get('user', instance.user)

        # Сохраняем обновленный объект в базе данных
        instance.save()

        return instance
    
        
    

# class JobsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Jobs
#         fields = ('__all__')



