from django.db import transaction

from .models import Advance, Student, Teacher, PersonalInformation, HealthInformation, InstitutionalInformation, Gender, CivilState, Nationality, Rol 
from users.models import CustomUser

from rolepermissions.decorators import has_role_decorator
from rolepermissions.roles import get_user_roles, assign_role

# Recibe toda la información capturada en el formulario
@transaction.atomic
def RegisterStudentTransaction(data):
    student_rol = 'student'
    
    user = CustomUser.objects.create_user(
        username=data['email'].split("@")[0], # username
        email=data['email'], #email
        password=data['password'], #password
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    user.save()

    health_information = HealthInformation(
        grupo_sanguineo="A",
        rh="+",
        eps="famisanar"
    )
    health_information.save()

    personal_information = PersonalInformation(
        gender=Gender.objects.get(pk=data['gender']),
        birth_date=data['birth_date'],
        civil_state=CivilState.objects.get(pk=data['civil_state']),
        nationality=Nationality.objects.get(pk=data['nationality']),
        mobile=data['mobile'],
        health_information=health_information
    )
    personal_information.save()

    institutional_information = InstitutionalInformation(
        rol=Rol.objects.get(pk=data['rol']),
        cvlac=data['cvlac'],
        institutional_email=data['email']
    )
    institutional_information.save()
    
    student = Student(
        user = user,
        personal_information = personal_information,
        institutional_information = institutional_information
    )
    student.save()

    assign_role(user, student_rol)

    return True


def UpdateStudent(pk, data):
    print(data)
    student = Student.objects.get(pk=pk)
    if student is not None:
        print(student)
        persona_information = PersonalInformation.objects.get(pk=student.personal_information)
        institutional_information = InstitutionalInformation.objects.get(pk=student.personal_information)
        student.user.first_name = data["first_name"]
        student.user.last_name = data["last_name"]
        student.personal_information.mobile = data["mobile"]
        student.user.email = data["email"]
        student.personal_information.address = data["address"]
        student.personal_information.birth_date = data["birth_date"]
        student.institutional_information.cvlac = data["cvlac"]
        student.user.password = data["password"]
        
        # student.save()

        return student
    
    return None