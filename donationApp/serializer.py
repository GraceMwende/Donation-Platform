from rest_framework import serializers
from .models import Charity,Donor,Donations,CustomUser

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
    fields = ('__all__')
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
    fields = ('__all__')

  def create(self, validated_data):
        users_data = validated_data.pop('users')
        user = CustomUser.objects.create(**users_data)
        charity =  Charity.objects.create(users=user,**validated_data)
        return charity

        # charity = Charity.objects.create(**validated_data)
        # for user in users:
          # charity = CustomUser.objects.get(pk=user.get('id'))
          # instance.users.add(charity)
        # CustomUser.objects.create(charity=charity,**users)
        # return charity

  def update(self,instance,validated_data):
    users_data = validated_data.pop('users')
    users = instance.users

    instance.location = validated_data.get('location', instance.location)
    instance.save()

    users.user_name = users_data.get('user_name',users.user_name)

    users.first_name = users_data.get('first_name',users.first_name)
    users.last_name = users_data.get('last_name',users.last_name)
    users.email = users_data.get('email',users.email)
    users.save()

    return instance


  # def update (self,instance,validated_data):
  #   users = validated_data.pop('users')
  #   instance.location = validated_data.get('location',instance.location)
  #   instance.save()
  #   keep_users = []
  #   existing_ids = [u.id for u in instance.users]
  #   for user in users:
  #     if 'id' in user.keys():
  #       if CustomUser.objects.filter(id=user['id']).exists():
  #         u = CustomUser.objects.get(id=user['id'])
  #         u.last_name = user.get('last_name', u.last_name)
  #         u.save
  #         keep_users.append(u.id)

  #       else:
  #         continue

  #     else:
  #       u = CustomUser.objects.create(**user, charity=instance)
  #       keep_users.append(u.id)

  #   for user in instance.users:
  #     if user.id not in keep_users:
  #       user.delete()

  #   return instance



class DonationsSerializer(serializers.ModelSerializer,):
  donor = DonorSerializer()
  charity = CharitySerializer()
  class Meta:
    model = Donations
    fields = ('__all__')

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
