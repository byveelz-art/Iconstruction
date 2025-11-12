from django import forms
from .models import Herramienta, Material, Obra, Actividad, Usuario, Obrero

class HerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = '__all__'

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'

class ObraForm(forms.ModelForm):
    obrero = forms.ModelChoiceField(
        queryset=Obrero.objects.all(),
        required=True,
        label="Obrero asignado"
    )

    class Meta:
        model = Obra
        fields = ['direccion']  # no pedimos 'estado'

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = '__all__'

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class ObreroForm(forms.ModelForm):
    class Meta:
        model = Obrero
        fields = '__all__'
        labels = {
            'nombre_completo': 'Nombre completo del obrero',
        }