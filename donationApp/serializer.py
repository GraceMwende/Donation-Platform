from rest_framework import serializers
from .models import Charity,Donor,Donations,CustomUser,BenefactorsStories
import re


# class Base64ImageField(serializers.ImageField):
#   def to_internal_value(self, data,altchars=b'+/'):
#     from django.core.files.base import ContentFile
#     import base64
#     import six
#     import uuid

#       # Check if this is a base64 string
#     if isinstance(data, six.string_types):
#       if 'data:' in data and ';base64,' in data:
#         header, data = data.split(';base64,')

#       try:
#         data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
#         missing_padding = len(data) % 4
#         if missing_padding:
#           data += b'='* (4 - missing_padding)
#         return base64.b64decode(data, altchars)
            
#       except TypeError:
#         self.fail('invalid_image')

#       file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
#           # Get the file name extension:
#       file_extension = self.get_file_extension(file_name, decoded_file)

#       complete_file_name = "%s.%s" % (file_name, file_extension, )

#       data = ContentFile(decoded_file, name=complete_file_name)

#     return super(Base64ImageField, self).to_internal_value(data)

#   def get_file_extension(self, file_name, decoded_file):
#     import imghdr

#     extension = imghdr.what(file_name, decoded_file)
#     extension = "jpg" if extension == "jpeg" else extension

#     return extension

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

        # charity = Charity.objects.create(**validated_data)
        # for user in users:
          # charity = CustomUser.objects.get(pk=user.get('id'))
          # instance.users.add(charity)
        # CustomUser.objects.create(charity=charity,**users)
        # return charity

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
  # user_image = serializers.ImageField(required=False, use_url=True)
  # user_image = Base64ImageField(
  #       max_length=None, use_url=True,
  #   )

  class Meta:
    model = BenefactorsStories()
    fields = '__all__'

  def create(self, validated_data):
      charity_data = validated_data.pop('charity')
      charities = Charity.objects.create(**charity_data)
      benefactor =  Charity.objects.create(charity=charities,**validated_data)
      return benefactor

  def update(self,instance,validated_data):
    users_data = validated_data.pop('charity')
    charity = instance.charity

    instance.user_image = validated_data.get('user_image', instance.user_image)
    instance.title = validated_data.get('title', instance.title)
    instance.description = validated_data.get('description', instance.description)
    instance.save()

    charity.user_name = charity_data.get('user_name',charity.user_name)

    charity.first_name = charity_data.get('first_name',charity.first_name)
    charity.last_name = charity_data.get('last_name',charity.last_name)
    charity.email = charity_data.get('email',charity.email)
    charity.save()

    return instance