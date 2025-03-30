from django.contrib import admin

from animals.lostpetreporting.models import LostPetReport
from animals.models import Animal, AdoptionRequest, Donation
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'status', 'created_at')

@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'animal', 'status', 'created_at')

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'created_at')
    search_fields = ('user__username', 'transaction_id')
    list_filter = ('status',)

admin.site.register(LostPetReport)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'full_name', 'phone', 'address')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)