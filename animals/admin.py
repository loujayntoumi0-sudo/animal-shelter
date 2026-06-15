from django.contrib import admin
from .models import (
    Animal,
    Breed,
    Adopter,
    AnimalHealthRecord,
    Vet,
    Appointment,
    Medication,
    Prescription,
    ContactMessage,
    VetChatMessage,
)

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'race', 'age', 'gender', 'status', 'weight', 'height']
    list_filter = ['species', 'status', 'gender']
    search_fields = ['name', 'species']

    def race(self, obj):
        return obj.breed_text or (obj.breed.name if obj.breed else '')
    race.short_description = 'Race'

@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Adopter)
class AdopterAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'animal', 'created_at']
    list_filter = ['animal', 'created_at']
    search_fields = ['name', 'phone', 'address']

@admin.register(AnimalHealthRecord)
class AnimalHealthRecordAdmin(admin.ModelAdmin):
    list_display = ['animal', 'recorded_at', 'weight', 'height', 'condition']
    list_filter = ['recorded_at', 'condition']
    search_fields = ['animal__name', 'condition']

@admin.register(Vet)
class VetAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty', 'phone', 'email', 'active']
    list_filter = ['active', 'specialty']
    search_fields = ['name', 'specialty']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['animal', 'vet', 'appointment_date', 'reason', 'follow_up']
    list_filter = ['appointment_date', 'follow_up']
    search_fields = ['animal__name', 'vet__name', 'reason']

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'stock', 'price', 'for_species']
    search_fields = ['name', 'category', 'for_species']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['animal', 'medication', 'vet', 'dosage', 'start_date', 'end_date']
    search_fields = ['animal__name', 'medication__name', 'vet__name']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'resolved']
    list_filter = ['resolved', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']


@admin.register(VetChatMessage)
class VetChatMessageAdmin(admin.ModelAdmin):
    list_display = ['vet', 'sender_name', 'is_from_vet', 'created_at']
    list_filter = ['vet', 'is_from_vet', 'created_at']
    search_fields = ['sender_name', 'message']
