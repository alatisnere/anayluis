"""Siembra la demo de Ana & Luis: configuracion, usuario del dashboard e invitados de ejemplo."""
import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from invitations.models import AppConfig, Party, RSVP

FAMILIAS = [
    ("Familia Rivera Guzmán", 4), ("Familia Mendoza Salas", 4),
    ("Sr. y Sra. Ontiveros", 2), ("Familia Beltrán Ruiz", 5),
    ("Ana Karen y Diego", 2), ("Familia Zavala Nieto", 3),
    ("Mariana Cordero", 1), ("Familia Escobedo Lara", 4),
    ("Padrinos de velación", 2), ("Familia Quintero Ávila", 3),
    ("Sofía Palencia", 2), ("Familia Rendón Cabrera", 4),
    ("Emilio y Regina", 2), ("Familia Narváez Solís", 3),
    ("Tíos de Tepoztlán", 2), ("Familia Aguirre Peña", 4),
    ("Fernanda y Rodrigo", 2), ("Familia Villaseñor Rojo", 3),
    ("Compañeros de la oficina", 6), ("Familia Ibáñez Moreno", 4),
    ("Lucía Manrique", 1), ("Familia Cuevas Herrera", 3),
    ("Jorge y Paulina", 2), ("Familia Serrano Ochoa", 4),
    ("Amigos de la universidad", 6), ("Familia Trejo Bermúdez", 3),
    ("Andrea Villalobos", 2), ("Familia Duarte Espino", 4),
    ("Padrinos de anillos", 2), ("Familia Robles Andrade", 3),
    ("Camila y Sebastián", 2), ("Familia Uribe Cantú", 5),
    ("Ximena Otero", 1), ("Familia Fuentes Barrera", 3),
    ("Vecinos de la cuadra", 4), ("Familia Gallardo Ponce", 4),
    ("Natalia y Óscar", 2), ("Familia Bustos Reyna", 3),
    ("Renata Cisneros", 2), ("Familia Lozano Ferrer", 4),
]

TEXTO_CONFIRMA_SI = "¡Qué alegría! Ya quedaron confirmados todos sus lugares. Nos vemos el 21 de noviembre."
TEXTO_CONFIRMA_PARCIAL = "¡Gracias! Guardamos los lugares que nos confirmaron. Si algo cambia, pueden editar su respuesta."
TEXTO_CONFIRMA_NO = "Gracias por avisarnos. Los vamos a extrañar ese día."


class Command(BaseCommand):
    help = "Carga los datos de la demo (idempotente)."

    def handle(self, *args, **opts):
        rnd = random.Random(21112026)

        cfg = AppConfig.objects.filter(pk=1).first()
        if not cfg:
            cfg = AppConfig(pk=1)
        cfg.invite_password = "anayluis"
        cfg.rsvp_deadline = timezone.now() + timedelta(days=60)
        cfg.invite_message_template = (
            "Hola {nombre} 👋\nNos casamos y nos encantaría que nos acompañaran.\n"
            "Aquí pueden ver la invitación y confirmar: {link}"
        )
        cfg.confirm_text_yes = TEXTO_CONFIRMA_SI
        cfg.confirm_text_partial = TEXTO_CONFIRMA_PARCIAL
        cfg.confirm_text_no = TEXTO_CONFIRMA_NO
        cfg.rsvp_deadline_passed_text_yes = "Ya cerramos la lista. Su confirmación quedó registrada."
        cfg.rsvp_deadline_passed_text_partial = "Ya cerramos la lista con los lugares que nos confirmaron."
        cfg.rsvp_deadline_passed_text_no = "Ya cerramos la lista. Gracias por avisarnos."
        cfg.rsvp_deadline_passed_text_none = "El periodo de confirmación ya terminó. Escríbenos y lo vemos."
        cfg.restrictions_text = (
            "Con mucho cariño les pedimos que esta celebración sea solo para adultos, "
            "y que los lugares asignados a su invitación no se compartan."
        )
        cfg.save()

        if not Party.objects.exists():
            for nombre, boletos in FAMILIAS:
                p = Party.objects.create(
                    display_name=nombre,
                    max_tickets=boletos,
                    show_restrictions_text=rnd.random() < 0.35,
                )
                r = rnd.random()
                if r < 0.55:                      # confirman todo
                    RSVP.objects.create(party=p, response="YES", tickets_confirmed=boletos)
                elif r < 0.70:                    # confirman parcial
                    RSVP.objects.create(
                        party=p, response="YES",
                        tickets_confirmed=max(1, boletos - rnd.randint(1, max(1, boletos - 1))),
                    )
                elif r < 0.82:                    # no asisten
                    RSVP.objects.create(party=p, response="NO", tickets_confirmed=0)
                # el resto se queda sin responder

        User = get_user_model()
        if not User.objects.filter(username="demo").exists():
            User.objects.create_superuser("demo", "demo@esnuestrodia.com", "demo1234")

        self.stdout.write(self.style.SUCCESS(
            f"Demo lista: {Party.objects.count()} invitaciones, "
            f"{RSVP.objects.count()} respuestas."
        ))
