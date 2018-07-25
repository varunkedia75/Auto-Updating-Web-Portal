from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from . import models
from django.contrib.auth.models import User


def homepage(request, department):
    # template = loader.get_template('fpagecse/page22.html')
    # return HttpResponse(template.render())
    context = {
        'department': department,
    }
    return render(request, 'fpagecse/page22.html', context)


def all_faculty(request, department):
    faculty = models.Faculty.objects.all()
    template = loader.get_template('fpagecse/allfaculty.html')
    context = {
        'faculty': faculty,
        'department': department,
    }
    return HttpResponse(template.render(context, request))
    # return render(request, 'fpagecse/allfaculty.html', {'faculty': faculty})


def headofdepartment(request, department):
    faculty = models.Faculty.objects.all()
    template = loader.get_template('fpagecse/headofdepartment.html')
    context = {
        'faculty': faculty,
        'department': department,
    }
    return HttpResponse(template.render(context, request))


def prof(request, department):
    faculty = models.Faculty.objects.all()
    template = loader.get_template('fpagecse/prof.html')
    context = {
        'faculty': faculty,
        'department': department,
    }
    return HttpResponse(template.render(context, request))


def associate_prof(request, department):
    faculty = models.Faculty.objects.all()
    template = loader.get_template('fpagecse/associate_prof.html')
    context = {
        'faculty': faculty,
        'department': department,
    }
    return HttpResponse(template.render(context, request))


def assistant_prof(request, department):
    faculty = models.Faculty.objects.all()
    template = loader.get_template('fpagecse/assistant_prof.html')
    context = {
        'faculty': faculty,
        'department': department,
    }
    return HttpResponse(template.render(context, request))


def visiting_faculty(request, department):
    faculty = models.Faculty.objects.all()
    template = loader.get_template('fpagecse/visiting_faculty.html')
    context = {
        'faculty': faculty,
        'department': department,
    }
    return HttpResponse(template.render(context, request))


def facultypage(request, user):
    faculty = models.Faculty.objects.get(user=user)
    abc = User.objects.get(username=user)
    # lala = models.Students.objects.filter(user=user).filter(status="Continuing Student", degree="PHD")
    # a1 = ""
    # a2 = ""
    # for i in models.Students:
    #     if i.status == "Continuing Student":
    #         a1 = "Continuing Student"
    #     elif i.status == "Completed Student":
    #         a2 = "Completed Student"

    context = {
        'faculty': faculty,
        'usr': abc,
    }
    # return HttpResponse(context.user)
    return render(request, 'index.html', context)









