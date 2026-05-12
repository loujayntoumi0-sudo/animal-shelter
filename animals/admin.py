from django.contrib import admin
from .models import Animal, Breed, Adopter

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'race', 'age', 'gender', 'status']
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
