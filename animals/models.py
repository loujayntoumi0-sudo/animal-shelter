from django.db import models
from django.urls import reverse

class Breed(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom de la race")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Breed"
        verbose_name_plural = "Breeds"
        ordering = ['name']

class Animal(models.Model):

    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('rabbit', 'Rabbit'),
        ('bird', 'Bird'),
        ('other', 'Other'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available for Adoption'),
        ('adopted', 'Already Adopted'),
        ('medical', 'Medical Care'),
        ('reserved', 'Reserved for Adoption'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nom de l'animal")
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES, verbose_name="Espèce")
    breed = models.ForeignKey(
        Breed, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='animals',
        verbose_name="Race"
    )
    breed_text = models.CharField(max_length=100, blank=True, verbose_name="Race")
    age = models.IntegerField(help_text="Âge en mois", verbose_name="Âge (mois)")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Sexe")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Poids (kg)")
    color = models.CharField(max_length=50, blank=True, verbose_name="Couleur")
    description = models.TextField(blank=True, verbose_name="Description")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="Statut")
    arrival_date = models.DateField(auto_now_add=True, verbose_name="Date d'arrivée")
    medical_notes = models.TextField(blank=True, verbose_name="Notes médicales")
    is_vaccinated = models.BooleanField(default=False, verbose_name="Vacciné")
    is_neutered = models.BooleanField(default=False, verbose_name="Stérilisé")
    
    image = models.ImageField(
        upload_to='animal_photos/', 
        null=True, 
        blank=True, 
        verbose_name="Photo de l'animal"
    )

    def __str__(self):
        return f"{self.name} ({self.get_species_display()})"

    def get_absolute_url(self):
        return reverse('animal_list')

    def age_in_years(self):
        if self.age >= 12:
            return f"{self.age // 12} ans"
        return f"{self.age} mois"

    class Meta:
        ordering = ['-arrival_date']
        verbose_name = "Animal"
        verbose_name_plural = "Animals"


class Adopter(models.Model):
    name = models.CharField(max_length=120, verbose_name="Nom")
    address = models.TextField(verbose_name="Adresse")
    phone = models.CharField(max_length=30, verbose_name="Téléphone")
    animal = models.ForeignKey(
        Animal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='adopters',
        verbose_name="Animal souhaité"
    )
    notes = models.TextField(blank=True, verbose_name="Commentaire")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de la demande")

    def __str__(self):
        animal_label = self.animal.name if self.animal else 'Aucun animal sélectionné'
        return f"{self.name} → {animal_label}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.animal and self.animal.status != 'adopted':
            self.animal.status = 'adopted'
            self.animal.save(update_fields=['status'])

    def delete(self, *args, **kwargs):
        animal = self.animal
        if animal and animal.status == 'adopted':
            remaining = Adopter.objects.filter(animal=animal).exclude(pk=self.pk)
            if not remaining.exists():
                animal.status = 'available'
                animal.save(update_fields=['status'])
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Adoptant'
        verbose_name_plural = 'Adoptants'
