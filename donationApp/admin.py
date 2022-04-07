from django.contrib import admin
from .models import CustomUser,Charity,Donor,Donations,BenefactorsStory,Beneficiaries
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserAdminConfig(UserAdmin):
    model = CustomUser
    search_fields = ('email', 'user_name')
    list_filter = ('email', 'user_name', 'is_active', 'is_staff')
    ordering = ('-date_joined',)
    list_display = ('email', 'user_name',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'user_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        
    )
   
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name','last_name','first_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(CustomUser,UserAdminConfig)
admin.site.register(Charity)
admin.site.register(Donor)
admin.site.register(Donations)
admin.site.register(BenefactorsStory)
admin.site.register(Beneficiaries)