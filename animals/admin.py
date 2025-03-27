from django.contrib import admin

from animals.lostpetreporting.models import LostPetReport
from animals.models import Animal, AdoptionRequest, Donation

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