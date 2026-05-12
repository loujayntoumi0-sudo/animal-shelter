from django import forms
from .models import Animal, Breed, Adopter

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = [
            "name",
            "species",
            "breed_text",
            "age",
            "gender",
            "status",
            "description",
            "image",
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'animal'}),
            'species': forms.Select(attrs={'class': 'form-control'}),
            'breed_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Race de l\'animal'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Âge en mois'}),
            'gender': forms.RadioSelect(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
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
