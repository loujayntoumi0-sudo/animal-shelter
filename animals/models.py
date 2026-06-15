from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

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
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Hauteur (cm)")
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

    def bmi(self):
        if self.height and self.weight:
            height_m = float(self.height) / 100
            if height_m > 0:
                return round(float(self.weight) / (height_m ** 2), 1)
        return None

    def health_summary(self):
        bmi = self.bmi()
        if bmi is None:
            return 'Informations de santé incomplètes'
        if bmi < 10:
            return 'Poids insuffisant'
        if bmi <= 25:
            return 'Poids optimal'
        return 'Surpoids à surveiller'

    class Meta:
        ordering = ['-arrival_date']
        verbose_name = "Animal"
        verbose_name_plural = "Animals"


class AnimalHealthRecord(models.Model):
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='health_records',
        verbose_name='Animal'
    )
    recorded_at = models.DateField(default=timezone.now, verbose_name='Date de mesure')
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Poids (kg)')
    height = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Hauteur (cm)')
    condition = models.CharField(max_length=100, blank=True, verbose_name='Condition')
    notes = models.TextField(blank=True, verbose_name='Observations vétérinaires')

    class Meta:
        ordering = ['-recorded_at']
        verbose_name = 'Fiche de santé'
        verbose_name_plural = 'Fiches de santé'

    def __str__(self):
        return f"{self.animal.name} — {self.recorded_at}"


class Vet(models.Model):
    name = models.CharField(max_length=120, verbose_name='Nom du vétérinaire')
    specialty = models.CharField(max_length=120, blank=True, verbose_name='Spécialité')
    phone = models.CharField(max_length=30, blank=True, verbose_name='Téléphone')
    email = models.EmailField(blank=True, verbose_name='Email')
    active = models.BooleanField(default=True, verbose_name='Actif')
    notes = models.TextField(blank=True, verbose_name='Notes complémentaires')

    class Meta:
        ordering = ['name']
        verbose_name = 'Vétérinaire'
        verbose_name_plural = 'Vétérinaires'

    def __str__(self):
        return self.name


class Appointment(models.Model):
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Animal'
    )
    vet = models.ForeignKey(
        Vet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments',
        verbose_name='Vétérinaire'
    )
    appointment_date = models.DateTimeField(verbose_name='Date du rendez-vous')
    reason = models.CharField(max_length=200, verbose_name='Raison du rendez-vous')
    outcome = models.TextField(blank=True, verbose_name='Résultat / recommandations')
    follow_up = models.BooleanField(default=False, verbose_name='Suivi requis')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')

    class Meta:
        ordering = ['-appointment_date']
        verbose_name = 'Rendez-vous'
        verbose_name_plural = 'Rendez-vous'

    def __str__(self):
        return f"{self.animal.name} — {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"


class Medication(models.Model):
    name = models.CharField(max_length=150, verbose_name='Médicament / Produit')
    category = models.CharField(max_length=100, blank=True, verbose_name='Catégorie')
    stock = models.IntegerField(default=0, verbose_name='Stock disponible')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Prix (€)')
    description = models.TextField(blank=True, verbose_name='Description')
    for_species = models.CharField(max_length=100, blank=True, verbose_name='Espèces concernées')

    class Meta:
        ordering = ['name']
        verbose_name = 'Médicament'
        verbose_name_plural = 'Pharmacie'

    def __str__(self):
        return self.name


class Prescription(models.Model):
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='prescriptions',
        verbose_name='Animal'
    )
    medication = models.ForeignKey(
        Medication,
        on_delete=models.CASCADE,
        related_name='prescriptions',
        verbose_name='Médicament'
    )
    vet = models.ForeignKey(
        Vet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='prescriptions',
        verbose_name='Vétérinaire'
    )
    dosage = models.CharField(max_length=120, verbose_name='Dosage')
    start_date = models.DateField(verbose_name='Début du traitement')
    end_date = models.DateField(blank=True, null=True, verbose_name='Fin du traitement')
    notes = models.TextField(blank=True, verbose_name='Instructions')

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Prescription'
        verbose_name_plural = 'Prescriptions'

    def __str__(self):
        return f"{self.medication.name} pour {self.animal.name}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120, verbose_name='Nom')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=180, verbose_name='Objet')
    message = models.TextField(verbose_name='Message')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    resolved = models.BooleanField(default=False, verbose_name='Traité')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Message de contact'
        verbose_name_plural = 'Messages de contact'

    def __str__(self):
        return f"{self.subject} — {self.name}"


class VetChatMessage(models.Model):
    vet = models.ForeignKey(
        Vet,
        on_delete=models.CASCADE,
        related_name='chat_messages',
        verbose_name='Vétérinaire'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Utilisateur'
    )
    sender_name = models.CharField(max_length=120, verbose_name="Nom de l'expéditeur")
    is_from_vet = models.BooleanField(default=False, verbose_name='Message du vétérinaire')
    message = models.TextField(verbose_name='Message')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Message de discussion'
        verbose_name_plural = 'Messages de discussion'

    def __str__(self):
        return f"{self.sender_name} — {self.vet.name} ({self.created_at:%d/%m/%Y %H:%M})"


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
