import uuid

from django.core.validators import MinValueValidator
from django.db import models


class AppConfig(models.Model):
    invite_password = models.CharField(max_length=64)

    rsvp_deadline = models.DateTimeField()

    invite_message_template = models.TextField()

    confirm_text_yes = models.TextField()
    confirm_text_partial = models.TextField()
    confirm_text_no = models.TextField()

    rsvp_deadline_passed_text_yes = models.TextField()
    rsvp_deadline_passed_text_partial = models.TextField()
    rsvp_deadline_passed_text_no = models.TextField()
    rsvp_deadline_passed_text_none = models.TextField()

    restrictions_text = models.TextField()

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "AppConfig"

    @classmethod
    def get_solo(cls):
        return cls.objects.filter(pk=1).first()


class Party(models.Model):
    code = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )
    display_name = models.CharField(max_length=200)
    max_tickets = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    phone_e164 = models.CharField(
        max_length=20,
        blank=True,
        default="",
    )

    show_restrictions_text = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.display_name} ({self.max_tickets})"


class RSVP(models.Model):
    class Response(models.TextChoices):
        YES = "YES", "Sí asisto"
        NO = "NO", "No asisto"

    party = models.OneToOneField(
        Party,
        on_delete=models.CASCADE,
        related_name="rsvp",
    )
    response = models.CharField(
        max_length=3,
        choices=Response.choices,
        null=True,
        blank=True,
    )
    tickets_confirmed = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.tickets_confirmed > self.party.max_tickets:
            from django.core.exceptions import ValidationError

            raise ValidationError(
                {"tickets_confirmed": "No puede exceder los boletos asignados."}
            )

    def __str__(self) -> str:
        return f"{self.party.display_name}: {self.response} ({self.tickets_confirmed})"
