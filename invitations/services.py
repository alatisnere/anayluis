import urllib.parse
from dataclasses import dataclass


@dataclass(frozen=True)
class PartyStatus:
    key: str
    label: str


STATUS_NO_RESPONSE = PartyStatus("NO_RESPONSE", "No response")
STATUS_ACCEPTED = PartyStatus("ACCEPTED", "Accepted")
STATUS_PARTIAL = PartyStatus("PARTIAL", "Partially accepted")
STATUS_DECLINED = PartyStatus("DECLINED", "Declined")


def compute_status(party) -> PartyStatus:
    rsvp = getattr(party, "rsvp", None)

    if not rsvp:
        return STATUS_NO_RESPONSE

    if rsvp.response == "NO":
        return STATUS_DECLINED

    if rsvp.tickets_confirmed >= party.max_tickets:
        return STATUS_ACCEPTED

    if 0 < rsvp.tickets_confirmed < party.max_tickets:
        return STATUS_PARTIAL

    return STATUS_NO_RESPONSE


def build_whatsapp_text(party, rsvp_url: str) -> str:
    return (
        f"Hello {party.display_name} 👋\n"
        f"Please confirm your attendance here:\n"
        f"{rsvp_url}\n"
    )


def build_wa_me_link(phone_e164: str, text: str):
    if not phone_e164:
        return None

    encoded = urllib.parse.quote(text)
    return f"https://wa.me/{phone_e164}?text={encoded}"
