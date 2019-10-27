from django.db import transaction

from .models import Advance, Student, Teacher, PersonalInformation, HealthInformation, InstitutionalInformation, Gender, CivilState, Nationality, Advance, Thesis
from users.models import CustomUser

from rolepermissions.decorators import has_role_decorator
from rolepermissions.roles import get_user_roles, assign_role

# Recibe toda la información capturada en el formulario
@transaction.atomic
def RegisterStudentTransaction(data, photo):
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
        address=data['address'],
        health_information=health_information,
        photo=photo
    )
    personal_information.save()

    institutional_information = InstitutionalInformation(
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

@transaction.atomic
def UpdateStudent(user_id, data, photo):
    student = Student.objects.get(user=user_id)
    if student is not None:
        student.user.first_name = data["first_name"]
        student.user.last_name = data["last_name"]
        student.user.email = data["email"]
        student.personal_information.gender = Gender.objects.get(pk=data["gender"])
        student.personal_information.birth_date = data["birth_date"]
        student.personal_information.civil_state = CivilState.objects.get(pk=data["civil_state"])
        student.personal_information.nationality = Nationality.objects.get(pk=data["nationality"])
        student.personal_information.address = data["address"]
        student.personal_information.mobile = data["mobile"]
        student.personal_information.photo = photo
        student.institutional_information.cvlac = data["cvlac"]
        student.personal_information.save()
        student.institutional_information.save()
        student.user.save()
        student.save()
        return True
    
    return None

# Recibe toda la información capturada en el formulario
@transaction.atomic
def RegisterTeacherTransaction(data, photo):
    teacher_rol = 'teacher'
    
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
        address=data['address'],
        health_information=health_information,
        photo=photo
    )
    personal_information.save()

    institutional_information = InstitutionalInformation(
        cvlac=data['cvlac'],
        institutional_email=data['email']
    )
    institutional_information.save()
    
    teacher = Teacher(
        user = user,
        personal_information = personal_information,
        institutional_information = institutional_information
    )
    teacher.save()

    assign_role(user, teacher_rol)

    return True

def UpdateTeacher(user_id, data, photo):
    teacher = Teacher.objects.get(user=user_id)
    if teacher is not None:
        print(photo)
        teacher.user.first_name = data["first_name"]
        teacher.user.last_name = data["last_name"]
        teacher.user.email = data["email"]
        teacher.personal_information.gender = Gender.objects.get(pk=data["gender"])
        teacher.personal_information.birth_date = data["birth_date"]
        teacher.personal_information.civil_state = CivilState.objects.get(pk=data["civil_state"])
        teacher.personal_information.nationality = Nationality.objects.get(pk=data["nationality"])
        teacher.personal_information.address = data["address"]
        teacher.personal_information.mobile = data["mobile"]
        teacher.personal_information.photo = photo
        teacher.institutional_information.cvlac = data["cvlac"]
        teacher.personal_information.save()
        teacher.institutional_information.save()
        teacher.user.save()
        teacher.save()
        return True
    
    return None

def RegisterAdvance(data):
    thesis = Thesis.objects.get(pk=data["thesis"])
    actual_advance = sum(advance.percentage for advance in Advance.objects.filter(thesis=thesis))
    if actual_advance + data["percentage"] <= 100:  
        advance = Advance(
            thesis=thesis,
            description=data["description"],
            percentage=data["percentage"],
            period=data["period"],
            observation=data["observation"]
        )
        if advance.save():
            return True
    return False