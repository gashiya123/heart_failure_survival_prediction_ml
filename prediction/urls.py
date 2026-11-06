
from django.urls import path

from .views import (
    home,
    admin_login,
    admin_dashboard,
    admin_logout,
    doctor_login,
    dashboard,
    add_doctor,
    manage_patients,
add_patient,
edit_patient,
delete_patient,
admin_prediction_history,
    search_patient,
    prediction_form,
    prediction_history,
    doctor_logout,
)

urlpatterns = [
    # Home
    path("", home, name="home"),

    # Admin
    path("admin-login/", admin_login, name="admin_login"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin-logout/", admin_logout, name="admin_logout"),

    path("add-doctor/", add_doctor, name="add_doctor"),
    path("manage-patients/", manage_patients, name="manage_patients"),
path("add-patient/", add_patient, name="add_patient"),
path("edit-patient/<int:patient_id>/", edit_patient, name="edit_patient"),
path("delete-patient/<int:patient_id>/", delete_patient, name="delete_patient"),
path(
    "admin-prediction-history/",
    admin_prediction_history,
    name="admin_prediction_history"
),

    # Doctor
    path("login/", doctor_login, name="doctor_login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("search-patient/", search_patient, name="search_patient"),
    path("prediction/<int:patient_id>/", prediction_form, name="prediction_form"),
    path("prediction-history/", prediction_history, name="prediction_history"),
    path("logout/", doctor_logout, name="doctor_logout"),
]
