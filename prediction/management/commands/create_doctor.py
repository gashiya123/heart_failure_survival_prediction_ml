from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from prediction.models import Doctor


class Command(BaseCommand):

    def handle(self,*args,**kwargs):

        name=input("doctor name: ")
        username=input("username: ")
        password=input("password: ")

        if Doctor.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR("username already exists"))
            return

        Doctor.objects.create(
            name=name,
            username=username,
            password=make_password(password)
        )

        self.stdout.write(
            self.style.SUCCESS("doctor created successfully")
        )