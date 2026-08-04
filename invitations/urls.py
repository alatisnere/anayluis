from django.urls import path

from . import views

urlpatterns = [
    # Public
    path("", views.home, name="home"),
    path("acceso/", views.gate, name="acceso"),
    path("salir/", views.logout_invite, name="invite_logout"),
    path("rsvp/<uuid:code>/", views.rsvp_detail, name="rsvp_detail"),

    # Auth (dashboard)
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/config/", views.app_config, name="app_config"),
    path("dashboard/export.csv", views.export_csv, name="export_csv"),

    # Dashboard: Parties
    path("dashboard/party/create/", views.party_create, name="party_create"),
    path("dashboard/party/upload/", views.party_upload_csv, name="party_upload_csv"),
    path("dashboard/party/template.xlsx", views.party_template_xlsx, name="party_template_xlsx"),
    path("dashboard/party/<int:party_id>/update/", views.party_update, name="party_update"),
    path("dashboard/party/<int:party_id>/delete/", views.party_delete, name="party_delete"),
]
