from django import forms
from .models import (
    Animal,
    Breed,
    Adopter,
    Vet,
    Medication,
    AnimalHealthRecord,
    ContactMessage,
    VetChatMessage,
)

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = [
            'name',
            'species',
            'breed',
            'breed_text',
            'age',
            'gender',
            'weight',
            'height',
            'status',
            'color',
            'is_vaccinated',
            'is_neutered',
            'medical_notes',
            'description',
            'image',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'animal'}),
            'species': forms.Select(attrs={'class': 'form-control'}),
            'breed': forms.Select(attrs={'class': 'form-control'}),
            'breed_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Race de l\'animal'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Âge en mois'}),
            'gender': forms.RadioSelect(),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Poids en kg'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Hauteur en cm'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Couleur'}),
            'is_vaccinated': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_neutered': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'medical_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notes médicales, diagnostics et recommandations'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description générale de l\'animal'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and not self.initial.get('breed_text'):
            if not self.instance.breed_text and self.instance.breed:
                self.initial['breed_text'] = self.instance.breed.name


class AdopterForm(forms.ModelForm):
    class Meta:
        model = Adopter
        fields = [
            'name',
            'address',
            'phone',
            'animal',
            'notes',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom complet'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Adresse complète'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'animal': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notes ou préférences supplémentaires'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = Animal.objects.exclude(status='adopted')
        if self.instance and self.instance.pk and self.instance.animal:
            queryset = Animal.objects.exclude(status='adopted') | Animal.objects.filter(pk=self.instance.animal.pk)
        self.fields['animal'].queryset = queryset

    def clean_animal(self):
        animal = self.cleaned_data.get('animal')
        if animal and animal.status == 'adopted':
            raise forms.ValidationError('Cet animal est déjà adopté et ne peut pas être sélectionné.')
        return animal


class BreedForm(forms.ModelForm):
    class Meta:
        model = Breed
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la race'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description de la race (facultatif)'}),
        }


class VetForm(forms.ModelForm):
    class Meta:
        model = Vet
        fields = ['name', 'specialty', 'phone', 'email', 'active', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du vétérinaire'}),
            'specialty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Spécialité'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notes complémentaires (horaires, spécialités, disponibilités)'}),
        }


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'category', 'stock', 'price', 'for_species', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du produit'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Catégorie'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantité disponible'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix (€)'}),
            'for_species': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Espèces concernées'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description du produit, usage et remises éventuelles'}),
        }


class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = AnimalHealthRecord
        fields = ['animal', 'recorded_at', 'weight', 'height', 'condition', 'notes']
        widgets = {
            'animal': forms.Select(attrs={'class': 'form-control'}),
            'recorded_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Poids en kg'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Hauteur en cm'}),
            'condition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'État de santé général'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observations du vétérinaire'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sujet du message'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Votre message'}),
        }


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = VetChatMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Écrire un message...'}),
        }
