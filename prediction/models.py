from django.db import models


class Doctor(models.Model):
    name=models.CharField(max_length=100)
    username=models.CharField(max_length=100,unique=True)
    password=models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Patient(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    sex=models.IntegerField()
    contact=models.CharField(max_length=20)

    def __str__(self):
        return self.name


class PredictionHistory(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)

    age=models.IntegerField()
    anaemia=models.IntegerField()
    creatinine_phosphokinase=models.IntegerField()
    diabetes=models.IntegerField()
    ejection_fraction=models.IntegerField()
    high_blood_pressure=models.IntegerField()
    platelets=models.FloatField()
    serum_creatinine=models.FloatField()
    serum_sodium=models.IntegerField()
    sex=models.IntegerField()
    smoking=models.IntegerField()
    time=models.IntegerField()

    prediction=models.IntegerField()
    probability=models.FloatField()

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - Prediction"