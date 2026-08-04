from django import forms
from django.utils import timezone

from .models import AppConfig, Party, RSVP


class RSVPForm(forms.Form):
    response = forms.ChoiceField(
        choices=RSVP.Response.choices,
        widget=forms.RadioSelect,
        initial=RSVP.Response.YES,
    )
    tickets_confirmed = forms.IntegerField(min_value=0, required=False)

    def __init__(self, *args, max_tickets: int, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_tickets = max_tickets

        self.fields["tickets_confirmed"].widget.attrs.update(
            {
                "min": 0,
                "max": max_tickets,
                "class": "border rounded px-3 py-2 w-32",
                "inputmode": "numeric",
            }
        )
        self.fields["tickets_confirmed"].help_text = f"Max: {max_tickets}"

        self.fields["response"].widget.attrs.update({"class": "space-y-1"})

    def clean(self):
        cleaned = super().clean()
        response = cleaned.get("response")
        tickets = cleaned.get("tickets_confirmed")

        if response == RSVP.Response.NO:
            cleaned["tickets_confirmed"] = 0
            return cleaned

        if tickets is None:
            self.add_error("tickets_confirmed", "Este campo es requerido.")
            return cleaned

        if tickets < 1:
            self.add_error("tickets_confirmed", "Debe ser al menos 1.")

        if tickets > self.max_tickets:
            self.add_error(
                "tickets_confirmed",
                f"No puede ser mayor a {self.max_tickets}.",
            )

        return cleaned


class PartyCreateForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ["display_name", "max_tickets", "phone_e164", "show_restrictions_text"]
        widgets = {
            "display_name": forms.TextInput(
                attrs={
                    "class": "w-full border border-black/10 rounded-xl px-4 py-2 bg-white",
                }
            ),
            "max_tickets": forms.NumberInput(
                attrs={
                    "class": "w-full border border-black/10 rounded-xl px-4 py-2 bg-white",
                    "min": 1,
                }
            ),
            "phone_e164": forms.TextInput(
                attrs={
                    "class": "w-full border border-black/10 rounded-xl px-4 py-2 bg-white",
                    "placeholder": "521XXXXXXXXXX (sin +)",
                }
            ),
            "show_restrictions_text": forms.CheckboxInput(
                attrs={"class": "h-4 w-4 rounded border-black/20"}
            ),
        }


class PartyCSVUploadForm(forms.Form):
    file = forms.FileField()


class AppConfigForm(forms.ModelForm):
    class Meta:
        model = AppConfig
        fields = [
            "invite_password",
            "rsvp_deadline",
            "invite_message_template",
            "confirm_text_yes",
            "confirm_text_partial",
            "confirm_text_no",
            "rsvp_deadline_passed_text_yes",
            "rsvp_deadline_passed_text_partial",
            "rsvp_deadline_passed_text_no",
            "rsvp_deadline_passed_text_none",
            "restrictions_text",
        ]
        widgets = {
            "invite_password": forms.TextInput(
                attrs={
                    "class": "w-full border border-black/10 rounded-xl px-4 py-2 bg-white",
                    "placeholder": "Ej: frase_secreta_123",
                }
            ),
            "rsvp_deadline": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "w-full border border-black/10 rounded-xl px-4 py-2 bg-white",
                    "required": True,
                }
            ),
            "invite_message_template": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "w-full border border-black/10 rounded-xl px-4 py-2 bg-white",
                    "required": True,
                    "placeholder": "Ej: ¡Hola! Por favor confirma aquí: {link}",
                }
            ),
            "confirm_text_yes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "w-full border border-black/10 rounded-xl px-4 py-2 bg-white",
                    "required": True,
                    "placeholder": "Ej: ¡Gracias! Tu asistencia quedó confirmada ✅",
                }
            ),
            "confirm_text_partial": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "w-full border border-black/10 rounded-xl px-4 py-2 bg-white",
                    "required": True,
                    "placeholder": "Ej: ¡Gracias! Confirmamos tu asistencia parcial ✅",
                }
            ),
            "confirm_text_no": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "w-full border border-black/10 rounded-xl px-4 py-2 bg-white",
                    "required": True,
                    "placeholder": "Ej: Gracias por avisarnos. Te vamos a extrañar 💛",
                }
            ),
            "rsvp_deadline_passed_text_yes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "w-full border border-black/10 rounded-xl px-4 py-2 bg-white",
                    "required": True,
                    "placeholder": "Ej: Gracias por tu respuesta. El periodo de confirmación ya terminó.",
                }
            ),
            "rsvp_deadline_passed_text_partial": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "w-full border border-black/10 rounded-xl px-4 py-2 bg-white",
                    "required": True,
                    "placeholder": "Ej: Gracias por tu respuesta. El periodo de confirmación ya terminó.",
                }
            ),
            "rsvp_deadline_passed_text_no": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "w-full border border-black/10 rounded-xl px-4 py-2 bg-white",
                    "required": True,
                    "placeholder": "Ej: Gracias por avisarnos. El periodo de confirmación ya terminó.",
                }
            ),
            "rsvp_deadline_passed_text_none": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "w-full border border-black/10 rounded-xl px-4 py-2 bg-white",
                    "required": True,
                    "placeholder": (
                        "Ej: Gracias por tu interés. El periodo de confirmación ya terminó "
                        "y ya no es posible responder."
                    ),
                }
            ),
            "restrictions_text": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "w-full border border-black/10 rounded-xl px-4 py-2 bg-white",
                    "required": True,
                    "placeholder": "Ej: Te recordamos que este evento es solo para adultos.",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for f in self.fields.values():
            f.required = True

        if self.instance and self.instance.pk and self.instance.rsvp_deadline:
            local_dt = timezone.localtime(self.instance.rsvp_deadline)
            self.initial["rsvp_deadline"] = local_dt.strftime("%Y-%m-%dT%H:%M")

    def clean_invite_message_template(self):
        txt = (self.cleaned_data.get("invite_message_template") or "").strip()
        if "{link}" not in txt:
            raise forms.ValidationError(
                'El texto debe incluir "{link}" para insertar el link del RSVP.'
            )
        return txt

    def clean_rsvp_deadline(self):
        dt = self.cleaned_data.get("rsvp_deadline")
        if dt is None:
            return dt

        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())

        return dt
