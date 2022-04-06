from rest_framework import serializers
from .models import Charity,Donor,Donations,CustomUser,BenefactorsStories
from django.contrib.auth.hashers import make_password

class UsersSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField(required=False)
  class Meta:
    model = CustomUser
    exclude = ['is_staff','is_active','is_superuser','groups','user_permissions','last_login']

class DonorSerializer(serializers.ModelSerializer):
  donor = UsersSerializer()
  # groups = UsersSerializer(source='donations_set',many=True)
  class Meta:
    model = Donor
    fields = '__all__'
    # exclude = ['is_staff','is_active','is_superuser','groups','user_permissions','last_login']


  def create(self, validated_data):
      donor_data = validated_data.pop('donor')
      donors = CustomUser.objects.create(**donor_data)
      donor =  Donor.objects.create(donor=donors,**validated_data)
      return donor


  def update(self,instance,validated_data):
    donor_data = validated_data.pop('donor')
    donor = instance.donor

    # instance.location = validated_data.get('location', instance.location)
    # instance.save()

    donor.user_name = donor_data.get('user_name',donor.user_name)

    donor.first_name = donor_data.get('first_name',donor.first_name)
    donor.last_name = donor_data.get('last_name',donor.last_name)
    donor.email = donor_data.get('email',donor.email)
    donor.save()

    return instance



class CharitySerializer(serializers.ModelSerializer):
  users = UsersSerializer()
  class Meta:
    model = Charity
    fields = '__all__'

  def create(self, validated_data):
        users_data = validated_data.pop('users')
        user = CustomUser.objects.create(**users_data)
        charity =  Charity.objects.create(users=user,**validated_data)
        return charity


  def update(self,instance,validated_data):
    charity_data = validated_data.pop('users')
    users = instance.users

    instance.location = validated_data.get('location', instance.location)
    instance.save()

    users.user_name = charity_data.get('user_name',users.user_name)

    users.first_name = charity_data.get('first_name',users.first_name)
    users.last_name = charity_data.get('last_name',users.last_name)
    users.email = charity_data.get('email',users.email)
    users.save()

    return instance


class DonationsSerializer(serializers.ModelSerializer,):
  donor = DonorSerializer()
  charity = CharitySerializer()
  class Meta:
    model = Donations
    fields = '__all__'

  def create(self, validated_data):
      donor_data = validated_data.pop('donor')
      charity_data = validated_data.pop('charity')
      donors = Donor.objects.create(**donor_data)
      charitys = Charity.objects.create(**charity_data)
      charity_donor =  Donations.objects.create(donor=donors,charity=charitys, **validated_data)
      return charity_donor

# for user in users:
          # charity = CustomUser.objects.get(pk=user.get('id'))
          # instance.users.add(charity)
        # CustomUser.objects.create(charity=charity,**users)

class BenefactorSerializer(serializers.ModelSerializer):
  charity = CharitySerializer()

  class Meta:
    model = BenefactorsStories
    fields = '__all__'

  def create(self, validated_data):
      charity_data = validated_data.pop('charity')
      # started here
      data = charity_data['users']

      user_name = data['user_name']
      email = data['email']
      first_name = data['first_name']
      last_name = data['last_name']
      password = make_password(data['password'])

      new_user = CustomUser.objects.create(user_name=user_name, email=email, first_name=first_name, last_name=last_name, password=password)
      
      location = charity_data['location']
      charity_image = charity_data['charity_image']

      charities = Charity.objects.create(users=new_user, location=location, charity_image=charity_image)

      benefactor =  BenefactorsStories.objects.create(charity=charities,**validated_data)
      # charities = Charity.objects.create(**charity_data)
      # benefactor =  BenefactorsStories.objects.create(charity=charities,**validated_data)
      
      return benefactor

  def update(self,instance,validated_data):
    charity_data = validated_data.pop('charity')
    # starts here
    data = charity_data['users']
    users = instance.charity.users
    charity = instance.charity

    instance.charity = validated_data.get('charity', instance.charity)
    instance.user_image = validated_data.get('user_image', instance.user_image)
    instance.title = validated_data.get('title', instance.title)
    instance.description = validated_data.get('description', instance.description)
    instance.save()

    charity.location = charity_data.get('location', charity.location)
    charity.charity_image = charity_data.get('charity_image', charity.charity_image)
    charity.save()

    users.user_name = data.get('user_name', users.user_name)

    users.first_name = data.get('first_name', users.first_name)
    users.last_name = data.get('last_name', users.last_name)
    users.email = data.get('email', users.email)
    users.save()


    # charity = instance.charity
    # instance.user_image = validated_data.get('user_image', instance.user_image)
    # instance.title = validated_data.get('title', instance.title)
    # instance.description = validated_data.get('description', instance.description)
    # instance.save()

    # charity.user_name = users_data.get('user_name',charity.user_name)

    # charity.first_name = users_data.get('first_name',charity.first_name)
    # charity.last_name = users_data.get('last_name',charity.last_name)
    # charity.email = users_data.get('email',charity.email)
    # charity.save()

    return instance