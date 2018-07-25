from django.db import models
from django.contrib.auth.models import User


class Faculty(models.Model):
    user = models.CharField(max_length=300, default='1', primary_key=True)
    faculty_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300, default="")
    department = models.CharField(max_length=300)
    designation = models.CharField(max_length=250)
    phone = models.BigIntegerField()
    email = models.EmailField()
    room_no = models.CharField(max_length=20)
    photo = models.ImageField(default="facimages/default.jpg", upload_to="facimages")

    def __str__(self):
        return self.faculty_name


class Teaching(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    c_code = models.CharField(max_length=10)
    c_name = models.CharField(max_length=200)
    s_year = models.CharField(max_length=20)
    e_year = models.CharField(max_length=20)
    semester = models.CharField(max_length=10)


class Publications(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    p_title = models.CharField(max_length=200)
    date_of_p = models.CharField(max_length=20)
    other_info = models.CharField(max_length=500)


class Projects(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=200)
    funding_agency = models.CharField(max_length=500)
    s_year = models.CharField(max_length=20)
    e_year = models.CharField(max_length=20)
    pi = models.CharField(max_length=200)
    co_pi = models.CharField(max_length=200)


class Recognitions(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    recognition = models.CharField(max_length=500)
    presenter = models.CharField(max_length=500)
    year = models.CharField(max_length=20)


class Others(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    place = models.CharField(max_length=200)
    date = models.CharField(max_length=100)


class Invitedtalks(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    topic = models.CharField(max_length=500)
    invited_by = models.CharField(max_length=500)


class Responsibilities(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    responsibility = models.CharField(max_length=200)
    s_year = models.CharField(max_length=20)
    e_year = models.CharField(max_length=20)


class Work(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    designation = models.CharField(max_length=250)
    s_year = models.CharField(max_length=20)
    e_year = models.CharField(max_length=20)
    institute = models.CharField(max_length=250)
    department = models.CharField(max_length=200)


class Education(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    pass_year = models.CharField(max_length=20)
    department = models.CharField(max_length=200)
    institute = models.CharField(max_length=250)


class Research(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    topic = models.CharField(max_length=500)


class Students(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    degree = models.CharField(max_length=30)
    supervisor = models.CharField(max_length=200)
    scholar_name = models.CharField(max_length=200)
    thesis_title = models.CharField(max_length=200)


# class LoginUser(models.Model):
#     user = models.ForeignKey(Faculty, on_delete=models.CASCADE)
#
#
#     def __str__(self):
#         return self.username
