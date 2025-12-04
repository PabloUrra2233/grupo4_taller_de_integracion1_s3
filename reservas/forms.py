from django import forms
from .models import Reserva, BloqueHorario, DisponibilidadSala
from mesas.models import Mesa
import datetime


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["mesa", "fecha_reserva", "bloque", "comentario"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ordenar opciones de mesas y bloques
        self.fields["mesa"].queryset = Mesa.objects.filter(activa=True).select_related("sala")
        self.fields["mesa"].label_from_instance = lambda obj: f"{obj.sala.nombre} – Mesa {obj.numero_mesa}"
        self.fields["bloque"].queryset = BloqueHorario.objects.all().order_by("hora_inicio")
        self.fields["fecha_reserva"].widget.input_type = "date"

    def clean(self):
        cleaned_data = super().clean()
        mesa = cleaned_data.get("mesa")
        fecha = cleaned_data.get("fecha_reserva")
        bloque = cleaned_data.get("bloque")

        if not (mesa and fecha and bloque):
            return cleaned_data

        # 1) Verificar que la sala tenga disponibilidad ese día y bloque
        dia_semana = fecha.weekday()  # 0=lunes ... 6=domingo
        sala = mesa.sala
        existe_dispo = DisponibilidadSala.objects.filter(
            sala=sala,
            bloque=bloque,
            dia_semana=dia_semana,
            activa=True,
        ).exists()

        if not existe_dispo:
            raise forms.ValidationError(
                "La sala de esa mesa no tiene disponibilidad para ese día y bloque horario."
            )

        # 2) Evitar doble reserva de la misma mesa en mismo bloque/fecha
        ya_reservada = Reserva.objects.filter(
            mesa=mesa,
            fecha_reserva=fecha,
            bloque=bloque,
        ).exists()

        if ya_reservada:
            raise forms.ValidationError(
                "La mesa ya está reservada en ese horario."
            )

        return cleaned_data
