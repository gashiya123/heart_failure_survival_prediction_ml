import os
import joblib
import pandas as pd

from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password

from .models import Doctor,Patient,PredictionHistory
from django.contrib.auth import authenticate, login, logout
from .forms import DoctorLoginForm,AdminLoginForm,DoctorForm, PatientForm


# MODEL PATH

MODEL_PATH=os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "random_forest_model.pkl"
)

THRESHOLD_PATH=os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "random_forest_threshold.pkl"
)


# LOAD MODEL

model=joblib.load(MODEL_PATH)
threshold=joblib.load(THRESHOLD_PATH)

# HOME PAGE

def home(request):

    if "doctor_id" in request.session:

        return redirect("dashboard")

    return render(
        request,
        "prediction/home.html"
    )



# ADMIN LOGIN

def admin_login(request):

    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("admin_dashboard")

    if request.method == "POST":
        form = AdminLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None and user.is_superuser:
                login(request, user)
                return redirect("admin_dashboard")

            form.add_error(
                None,
                "Invalid admin username or password."
            )
    else:
        form = AdminLoginForm()

    return render(
        request,
        "prediction/admin_login.html",
        {"form": form}
    )



# ADMIN DASHBOARD

def admin_dashboard(request):

    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("admin_login")

    doctors = Doctor.objects.all().order_by("name")
    patients = Patient.objects.all().order_by("name")
    total_predictions = PredictionHistory.objects.count()

    return render(
        request,
        "prediction/admin_dashboard.html",
        {
            "doctors": doctors,
            "patients": patients,
            "total_doctors": doctors.count(),
            "total_patients": patients.count(),
            "total_predictions": total_predictions,
        }
    )



# ADD DOCTOR

def add_doctor(request):

    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("admin_login")

    if request.method == "POST":
        form = DoctorForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"].strip()
            username = form.cleaned_data["username"].strip()
            password = form.cleaned_data["password"]

            if not name or not username:
                form.add_error(None, "Name and username are required.")

            elif Doctor.objects.filter(username=username).exists():
                form.add_error("username", "This username already exists.")

            else:
                from django.contrib.auth.hashers import make_password

                Doctor.objects.create(
                    name=name,
                    username=username,
                    password=make_password(password)
                )

                return redirect("admin_dashboard")
    else:
        form = DoctorForm()

    return render(
        request,
        "prediction/add_doctor.html",
        {"form": form}
    )



# ADMIN ACCESS CHECK

def admin_required(request):
    return request.user.is_authenticated and request.user.is_superuser


# MANAGE PATIENTS

def manage_patients(request):
    if not admin_required(request):
        return redirect("admin_login")

    patients = Patient.objects.all().order_by("name")

    return render(
        request,
        "prediction/manage_patients.html",
        {"patients": patients}
    )


# ADD PATIENT

def add_patient(request):
    if not admin_required(request):
        return redirect("admin_login")

    if request.method == "POST":
        form = PatientForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"].strip()
            contact = form.cleaned_data["contact"].strip()

            if not name or not contact:
                form.add_error(
                    None,
                    "Name and contact are required."
                )
            else:
                Patient.objects.create(
                    name=name,
                    age=form.cleaned_data["age"],
                    sex=int(form.cleaned_data["sex"]),
                    contact=contact
                )

                messages.success(
                    request,
                    "Patient registered successfully."
                )
                return redirect("manage_patients")
    else:
        form = PatientForm()

    return render(
        request,
        "prediction/patient_form.html",
        {"form": form, "page_title": "Register Patient"}
    )


# EDIT PATIENT

def edit_patient(request, patient_id):
    if not admin_required(request):
        return redirect("admin_login")

    patient = Patient.objects.get(id=patient_id)

    initial_data = {
        "name": patient.name,
        "age": patient.age,
        "sex": str(patient.sex),
        "contact": patient.contact,
    }

    if request.method == "POST":
        form = PatientForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"].strip()
            contact = form.cleaned_data["contact"].strip()

            if not name or not contact:
                form.add_error(
                    None,
                    "Name and contact are required."
                )
            else:
                patient.name = name
                patient.age = form.cleaned_data["age"]
                patient.sex = int(form.cleaned_data["sex"])
                patient.contact = contact
                patient.save()

                messages.success(
                    request,
                    "Patient details updated successfully."
                )
                return redirect("manage_patients")
    else:
        form = PatientForm(initial=initial_data)

    return render(
        request,
        "prediction/patient_form.html",
        {
            "form": form,
            "page_title": "Edit Patient",
            "patient": patient,
        }
    )


# DELETE PATIENT

def delete_patient(request, patient_id):
    if not admin_required(request):
        return redirect("admin_login")

    patient = Patient.objects.get(id=patient_id)

    if request.method == "POST":
        # Preserve prediction history for patients who have predictions.
        if PredictionHistory.objects.filter(patient=patient).exists():
            messages.error(
                request,
                "This patient has prediction history and cannot be deleted."
            )
        else:
            patient.delete()
            messages.success(
                request,
                "Patient deleted successfully."
            )

        return redirect("manage_patients")

    return render(
        request,
        "prediction/delete_patient.html",
        {"patient": patient}
    )


# ADMIN PREDICTION HISTORY

def admin_prediction_history(request):
    if not admin_required(request):
        return redirect("admin_login")

    histories = PredictionHistory.objects.select_related(
        "patient", "doctor"
    ).order_by("-created_at")

    return render(
        request,
        "prediction/admin_prediction_history.html",
        {"histories": histories}
    )




# ADMIN LOGOUT

def admin_logout(request):
    logout(request)
    return redirect("home")



# DOCTOR LOGIN

def doctor_login(request):

    if request.method=="POST":

        form=DoctorLoginForm(request.POST)

        if form.is_valid():

            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]

            try:

                doctor=Doctor.objects.get(
                    username=username
                )

                if check_password(
                    password,
                    doctor.password
                ):

                    request.session["doctor_id"]=doctor.id

                    return redirect("dashboard")

                else:

                    form.add_error(
                        "password",
                        "incorrect password"
                    )

            except Doctor.DoesNotExist:

                form.add_error(
                    "username",
                    "doctor not found"
                )

    else:

        form=DoctorLoginForm()

    return render(
        request,
        "prediction/login.html",
        {"form":form}
    )


# DOCTOR DASHBOARD

def dashboard(request):

    if "doctor_id" not in request.session:

        return redirect("doctor_login")

    doctor=Doctor.objects.get(
        id=request.session["doctor_id"]
    )

    return render(
        request,
        "prediction/dashboard.html",
        {"doctor":doctor}
    )


# SEARCH PATIENT

def search_patient(request):

    if "doctor_id" not in request.session:

        return redirect("doctor_login")

    patients=[]

    search=request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        if search.isdigit():

            patients=Patient.objects.filter(
                id=int(search)
            )

        else:

            patients=Patient.objects.filter(
                name__icontains=search
            )

    return render(
        request,
        "prediction/search_patient.html",
        {
            "patients":patients,
            "search":search
        }
    )


# PREDICTION FORM

def prediction_form(request,patient_id):

    if "doctor_id" not in request.session:

        return redirect("doctor_login")

    patient=Patient.objects.get(
        id=patient_id
    )


    # HANDLE FORM SUBMISSION

    if request.method=="POST":

        age=int(
            request.POST["age"]
        )

        anaemia=int(
            request.POST["anaemia"]
        )

        creatinine_phosphokinase=int(
            request.POST["creatinine_phosphokinase"]
        )

        diabetes=int(
            request.POST["diabetes"]
        )

        ejection_fraction=int(
            request.POST["ejection_fraction"]
        )

        high_blood_pressure=int(
            request.POST["high_blood_pressure"]
        )

        platelets=float(
            request.POST["platelets"]
        )

        serum_creatinine=float(
            request.POST["serum_creatinine"]
        )

        serum_sodium=int(
            request.POST["serum_sodium"]
        )

        sex=int(
            request.POST["sex"]
        )

        smoking=int(
            request.POST["smoking"]
        )

        time=int(
            request.POST["time"]
        )


        # CREATE INPUT DATA

        data=pd.DataFrame([{

            "age":age,

            "anaemia":anaemia,

            "creatinine_phosphokinase":
                creatinine_phosphokinase,

            "diabetes":diabetes,

            "ejection_fraction":
                ejection_fraction,

            "high_blood_pressure":
                high_blood_pressure,

            "platelets":platelets,

            "serum_creatinine":
                serum_creatinine,

            "serum_sodium":
                serum_sodium,

            "sex":sex,

            "smoking":smoking,

            "time":time

        }])


        # GET PREDICTION PROBABILITY

        probability=model.predict_proba(
            data
        )[0][1]


        # APPLY THRESHOLD

        if probability>=threshold:

            prediction=1

        else:

            prediction=0


        # CONVERT PROBABILITY TO PERCENTAGE

        
        probability_percentage=f"{probability*100:.2f}"


        # GET DOCTOR

        doctor=Doctor.objects.get(
            id=request.session["doctor_id"]
        )


        # SAVE PREDICTION

        PredictionHistory.objects.create(

            patient=patient,

            doctor=doctor,

            age=age,

            anaemia=anaemia,

            creatinine_phosphokinase=
                creatinine_phosphokinase,

            diabetes=diabetes,

            ejection_fraction=
                ejection_fraction,

            high_blood_pressure=
                high_blood_pressure,

            platelets=platelets,

            serum_creatinine=
                serum_creatinine,

            serum_sodium=serum_sodium,

            sex=sex,

            smoking=smoking,

            time=time,

            prediction=prediction,

            probability=probability

        )

        probability_percentage=f"{probability*100:.2f}"
        # SHOW RESULT

        return render(

            request,

            "prediction/prediction_result.html",

            {
                "patient":patient,

                "prediction":prediction,

                "probability_percentage":
                    probability_percentage
            }

        )


    # SHOW FORM

    return render(

        request,

        "prediction/prediction_form.html",

        {
            "patient":patient
        }

    )


# PREDICTION HISTORY

def prediction_history(request):

    if "doctor_id" not in request.session:

        return redirect("doctor_login")

    doctor=Doctor.objects.get(
        id=request.session["doctor_id"]
    )

    histories=PredictionHistory.objects.filter(
        doctor=doctor
    ).order_by(
        "-created_at"
    )

    return render(

        request,

        "prediction/prediction_history.html",

        {
            "doctor":doctor,

            "histories":histories
        }

    )


# DOCTOR LOGOUT

def doctor_logout(request):

    request.session.flush()

    return redirect("doctor_login")