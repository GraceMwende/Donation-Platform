from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('',views.home, name='donate-home'),
  path('api/charities/',views.CharityList.as_view()),
  path('api/donors/',views.DonorList.as_view()),
  path('api/donations/',views.DonationsList.as_view()),
  path('api/users/',views.UsersList.as_view()),
  path('api/benefactor_stories/',views.BenefactorsList.as_view()),
  path('api/beneficiaries/',views.BeneficiaryList.as_view()),
  path('api/users/user-id/<int:pk>',views.UserDescription.as_view()),
  path('api/donors/donors-id/<int:pk>',views.DonorDescription.as_view()),
  path('api/donations/donations-id/<int:pk>',views.DonationsDescription.as_view()),
  path('api/beneficiary/beneficiary-id/<int:pk>',views.BeneficiaryDescription.as_view()),
  path('api/charities/charities-id/<int:pk>',views.CharityDescription.as_view()),
  path('api/benefactor_stories/benefactor-id/<int:pk>',views.BenefactorDescription.as_view()),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
