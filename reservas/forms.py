from django import forms
from .models import Reserva
from django.core.exceptions import ValidationError
from django.db.models import Q

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['mesa', 'fecha_reserva', 'hora_inicio', 'hora_fin', 'comentario']
        widgets = {
            'fecha_reserva': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'mesa': forms.Select(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        mesa = cleaned_data.get('mesa')
        fecha = cleaned_data.get('fecha_reserva')
        inicio = cleaned_data.get('hora_inicio')
        fin = cleaned_data.get('hora_fin')

        if inicio and fin and inicio >= fin:
            raise ValidationError("La hora de inicio debe ser anterior a la hora de fin.")

        if mesa and fecha and inicio and fin:
            # Check for overlaps
            # Overlap if: (StartA < EndB) and (EndA > StartB)
            overlaps = Reserva.objects.filter(
                mesa=mesa,
                fecha_reserva=fecha
            ).filter(
                Q(hora_inicio__lt=fin) & Q(hora_fin__gt=inicio)
            )
            
            if self.instance.pk:
                overlaps = overlaps.exclude(pk=self.instance.pk)

            if overlaps.exists():
                raise ValidationError("La mesa ya está reservada en ese horario.")
        
        return cleaned_data
