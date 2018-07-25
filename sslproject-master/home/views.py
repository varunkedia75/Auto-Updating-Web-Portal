import json
import urllib
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.views import generic
# from django.views.generic import View
# from .forms import Userform
# from django import forms
# from home.forms import MyFacultyForm
from .forms import UserForm
from fpagecse import models
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
import bs4
import re
import urllib.request
from django.contrib.auth.models import User


def homepage(request):
    sauce = urllib.request.urlopen('http://www.iitg.ac.in/home/newsmore/news').read()
    soup = bs4.BeautifulSoup(sauce, 'lxml')
    w = 200
    h = 10
    array1 = [[0 for x in range(w)] for y in range(h)]
    array2 = [[0 for x in range(w)] for y in range(h)]
    var = 0
    for news in soup.find_all('div', {"class": "newsarea"}):
        for x in news.find_all('a'):
            array1[var] = x['href']
            array2[var] = x.text
            var = var + 1
    # ram = soup.find_all('div', {"class" : "newsarea"})
    # shyam = soup.find_all('div', {"class" : "newsarea"}).find_all('a')
    context = {
        "x1": array1[0],
        "x2": array2[0],
        "y1": array1[1],
        "y2": array2[1],
        "z1": array1[2],
        "z2": array2[2],
    }
    return render(request, 'home/homepage.html', context)
    template = loader.get_template('home/homepage.html')
    return HttpResponse(template.render())


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        user = authenticate(username=username, password=password)
        if result['success']:
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('basic_info', {})
                else:
                    return render(request, 'home/login.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'home/login.html', {'error_message': 'Invalid login'})
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
    return render(request, 'home/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        # userx = request.POST['username']
        username = request.POST['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('login/basic_info')
        else:
            form = UserForm()
    context = {
        "form": form,
    }
    return render(request, 'home/signup.html', context)


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'home/login.html', context)


def basic_info(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    facul = models.Faculty.objects.filter(user=request.user)
    if not facul.exists():
        fac = ""
    else:
        fac = models.Faculty.objects.get(user=request.user)
    loo = request.user
    context = {
        'faculty': fac,
        'loo': loo,
    }

    return render(request, 'home/basic_info.html', context)


def basic(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    else:
        # user = request.user.id
        user = request.user
        # email = user.email
        # user = request.session.get('user')
        faculty_name = request.POST['faculty_name']
        department = request.POST['department']
        designation = request.POST['designation']
        phone = request.POST['phone']
        room_no = request.POST['room_no']
        email = request.POST['email']
        last_name = request.POST['last_name']
        photo = request.FILES.get('photo', 'facimages/def.png')
        facul = models.Faculty.objects.filter(user=request.user)
        if not facul.exists():
            faculty = models.Faculty(faculty_name=faculty_name, department=department, designation=designation,
                                     phone=phone, room_no=room_no, email=email, photo=photo,last_name=last_name)
            faculty.user = request.user
            # faculty.photo = photo
            faculty.save()
        else:
            models.Faculty.objects.filter(user=user).update(faculty_name=faculty_name, department=department,
                                                                      designation=designation, phone=phone,
                                                                      room_no=room_no, email=email, last_name=last_name)
            fac = models.Faculty.objects.get(user=user)
            fac.photo = photo
            fac.save()
        return HttpResponseRedirect('basic_info')


def teaching_page(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    template = loader.get_template('home/teaching.html')
    user = request.user
    return HttpResponse(template.render({'user': user}, request))


def teaching(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    else:
        c_code = request.POST['c_code']
        c_name = request.POST['c_name']
        s_year = request.POST['s_year']
        e_year = request.POST['e_year']
        semester = request.POST['semester']
        obj = models.Teaching(c_code=c_code, c_name=c_name, s_year=s_year, e_year=e_year, semester=semester)
        obj.user = request.user
        obj.save()
        return HttpResponseRedirect('teaching_page')


def teaching_crawler(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    else:
        abc = User.objects.get(username=request.user)
        aa = abc.username
        source = urllib.request.urlopen('http://www.iitg.ernet.in/cse/internet-pages/' + aa).read()
        soup = bs4.BeautifulSoup(source, 'lxml')
        for news in soup.find_all('div', {"data-content": "2"}):
            for x in news.find_all('div', {"class": "fh5co-icon"}):
                for c in x.find_all('li'):
                    i1 = c.text
                    i2 = i1.split("&diam;")[0]
                    i3 = i2.split('-')[1]
                    i2 = i2.split('-')[0]
                    i4 = i1.split("&diam;")[1]
                    i5 = i1.split(i4)[1]
                    i5 = i5[6:]
                    i6 = i5.split(':')[0]
                    i7 = i5.split(':')[1]
                    # print(i2)  # start
                    # print(i3)  # end
                    # print(i4)  # sem
                    # print(i6)  # course code
                    # print(i7)  # course name

                    print("\n")
                    obj = models.Teaching(c_code=i6, c_name=i7, s_year=i2, e_year=i3, semester=i4)
                    obj.user = request.user
                    obj.save()
        return HttpResponseRedirect('teaching_page')


def publications_page(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    template = loader.get_template('home/publications.html')
    return HttpResponse(template.render({}, request))


def publications(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    else:
        p_title = request.POST['p_title']
        date_of_p = request.POST['date_of_p']
        other_info = request.POST['other_info']
        obj = models.Publications(p_title=p_title, date_of_p=date_of_p, other_info=other_info)
        obj.user = request.user
        obj.save()
        return HttpResponseRedirect('publications_page')


def publication_crawler(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    else:
        abc = User.objects.get(username=request.user)
        aa = abc.username
        source = urllib.request.urlopen('http://www.iitg.ernet.in/cse/internet-pages/' + aa).read()
        soup = bs4.BeautifulSoup(source, 'lxml')
        for news in soup.find_all('div', {"data-content": "5"}):
            x = news.find('div', {"class": "fh5co-icon"})
            for c in x.find_all('li'):
                k = c.text
                y = k.split('"')[1].split('"')[0]  # title
                z = k.split(',')[-2] + "," + k.split(',')[-1]  # date
                w = k.split(y)[1].split(z)[0]  # others
                w = w[2:]
                w = w[:-1]
                obj = models.Publications(p_title=y, date_of_p=z, other_info=w)
                obj.user = request.user
                obj.save()
        return HttpResponseRedirect('publications_page')


def projects_page(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    template = loader.get_template('home/projects.html')
    return HttpResponse(template.render({}, request))


def projects(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    else:
        project_title = request.POST['project_title']
        funding_agency = request.POST['funding_agency']
        s_year = request.POST['s_year']
        e_year = request.POST['e_year']
        pi = request.POST['pi']
        co_pi = request.POST['co_pi']
        obj = models.Projects(project_title=project_title, funding_agency=funding_agency, s_year=s_year, e_year=e_year, pi=pi, co_pi=co_pi)
        obj.user = request.user
        obj.save()
        return HttpResponseRedirect('projects_page')


def project_crawler(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    else:
        abc = User.objects.get(username=request.user)
        aa = abc.username
        source = urllib.request.urlopen('http://www.iitg.ernet.in/cse/internet-pages/' + aa).read()
        soup = bs4.BeautifulSoup(source, 'lxml')
        for news in soup.find_all('div', {"data-content": "4"}):
            for x in news.find_all('div', {"class": "fh5co-icon"}):
                for c in x.find_all('p'):
                    j = c.text
                    i = [[0 for x in range(200)] for y in range(10)]
                    i2 = [[0 for x in range(200)] for y in range(10)]
                    k = 0
                    for b in c.find_all('strong'):
                        i[k] = b.text
                        k = k + 1

                    l = 0
                    m = 0
                    while l < k - 1:
                        i2[m] = j.split(i[l])[1].split(i[l + 1])[0]
                        # print(i2[m])
                        m = m + 1
                        l = l + 1
                    i2[m] = j.split(i[l])[1]
                    # print(i2[m])
                    i2[0] = i2[0][2:]
                    i2[0] = i2[0][:-1]
                    # print(i2[0])
                    if m == 3:
                        obj = models.Projects(project_title=i2[0], funding_agency=i2[2], s_year=i2[3],
                                              pi=i2[1])
                        obj.user = request.user
                        obj.save()
                    elif m == 4:
                        obj = models.Projects(project_title=i2[0], funding_agency=i2[2], s_year=i2[3], e_year=i2[4],
                                              pi=i2[1])
                        obj.user = request.user
                        obj.save()
                    else:
                        obj = models.Projects(project_title=i2[0], funding_agency=i2[3], s_year=i2[4], e_year=i2[5], pi=i2[1], co_pi=i2[2])
                        obj.user = request.user
                        obj.save()
        return HttpResponseRedirect('projects_page')


def students_page(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    template = loader.get_template('home/students.html')
    return HttpResponse(template.render({}, request))


def students(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    else:
        status = request.POST['status']
        degree = request.POST['degree']
        supervisor = request.POST['supervisor']
        scholar_name = request.POST['scholar_name']
        thesis_title = request.POST['thesis_title']
        obj = models.Students(status=status, degree=degree, supervisor=supervisor, scholar_name=scholar_name, thesis_title=thesis_title)
        obj.user = request.user
        obj.save()
        return HttpResponseRedirect('students_page')


def recognitions_page(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    template = loader.get_template('home/recognitions.html')
    return HttpResponse(template.render({}, request))


def recognitions(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    else:
        recognition = request.POST['recognition']
        presenter = request.POST['presenter']
        year = request.POST['year']
        obj = models.Recognitions(recognition=recognition, presenter=presenter, year=year)
        obj.user = request.user
        obj.save()
        return HttpResponseRedirect('recognitions_page')


def others_page(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    template = loader.get_template('home/others.html')
    return HttpResponse(template.render({}, request))


def others(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    else:
        name = request.POST['name']
        place = request.POST['place']
        date = request.POST['date']
        obj = models.Others(name=name, place=place, date=date)
        obj.user = request.user
        obj.save()
        return HttpResponseRedirect('others_page')


def invitedtalks(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    else:
        invited_by = request.POST['invited_by']
        topic = request.POST['topic']
        date = request.POST['date']
        obj = models.Invitedtalks(invited_by=invited_by, topic=topic, date=date)
        obj.user = request.user
        obj.save()
        return HttpResponseRedirect('others_page')


def responsibilities(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    else:
        responsibility = request.POST['responsibility']
        s_year = request.POST['s_year']
        e_year = request.POST['e_year']
        obj = models.Responsibilities(responsibility=responsibility, s_year=s_year, e_year=e_year)
        obj.user = request.user
        obj.save()
        return HttpResponseRedirect('others_page')


def work(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    else:
        designation = request.POST['designation']
        s_year = request.POST['s_year']
        e_year = request.POST['e_year']
        institute = request.POST['institute']
        department = request.POST['department']
        obj = models.Work(designation=designation, s_year=s_year, e_year=e_year, institute=institute, department=department)
        obj.user = request.user
        obj.save()
        return HttpResponseRedirect('basic_info')


# def work_crawler(request):
#     if not request.user.is_authenticated():
#         return render(request, 'home/login.html', {})
#     else:
#         abc = User.objects.get(username=request.user)
#         aa = abc.username
#         source = urllib.request.urlopen('http://jatinga.iitg.ernet.in/cseintranet/intranet-pages/' + aa).read()
#         soup = bs4.BeautifulSoup(source, 'lxml')
#         for news in soup.find_all('div', {"data-content": "1"}):
#             x = news.find_all('div', {"class": "fh5co-icon"})
#             if x.find('h4').get_text() == " Work Experiences":
#                 for c in x.find_all('p'):
#                     i1 = c.strong.text
#                     i2 = i1.split(',')[0]
#                     i3 = i1.split(i2)[1]
#                     i3 = i3[1:]
#                     # print(i2)  # Designation
#                     # print(i3)  # Department
#
#                     i4 = c.text
#                     i4 = i4.split(i1)[1]
#                     i4 = i4.strip()
#                     i5 = i4.split(',')[-1]
#                     i4 = i4.split(i5)[0]
#                     i4 = i4[:-1]
#                     i6 = i5.split('-')[0]
#                     i7 = i5.split('-')[1]
#
#                     # print(i4)  # inst
#                     # print(i6)  # start
#                     # print(i7)  # end
#
#                     obj = models.Work(designation=i2, s_year=i6, e_year=i7, institute=i4, department=i3)
#                     obj.user = request.user
#                     obj.save()
#         return HttpResponseRedirect('basic_info')


def education(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    else:
        degree = request.POST['degree']
        pass_year = request.POST['pass_year']
        department = request.POST['department']
        institute = request.POST['institute']
        obj = models.Education(degree=degree, pass_year=pass_year, department=department, institute=institute)
        obj.user = request.user
        obj.save()
        return HttpResponseRedirect('basic_info')


# def education_crawler(request):
#     return HttpResponseRedirect('basic_info')
#     if not request.user.is_authenticated():
#         return render(request, 'home/login.html', {})
#     else:
#         abc = User.objects.get(username=request.user)
#         aa = abc.username
#         source = urllib.request.urlopen('http://jatinga.iitg.ernet.in/cseintranet/intranet-pages/' + aa).read()
#         soup = bs4.BeautifulSoup(source, 'lxml')
#         for news in soup.find_all('div', {"data-content": "1"}):
#             x = news.find_all('div', {"class": "fh5co-icon"})
#             if x.find('h4').text == " Education":
#                 for c in x.find_all('li'):
#
#                     obj = models.Education(degree=y, pass_year=z, department=w, institute=r)
#                     obj.user = request.user
#                     obj.save()
#         return HttpResponseRedirect('basic_info')


def research(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login.html', {})
    else:
        topic = request.POST['topic']
        obj = models.Research(topic=topic)
        obj.user = request.user
        obj.save()
        return HttpResponseRedirect('basic_info')


def deletework(request):
    val = request.POST['deleteid']
    obj = models.Work.objects.get(id=val)
    obj.delete()
    return HttpResponseRedirect('basic_info')


def deleteedu(request):
    val = request.POST['deleteid']
    obj = models.Education.objects.get(id=val)
    obj.delete()
    return HttpResponseRedirect('basic_info')


def deleteinterest(request):
    val = request.POST['deleteid']
    obj = models.Research.objects.get(id=val)
    obj.delete()
    return HttpResponseRedirect('basic_info')


def deleteteaching(request):
    val = request.POST['deleteid']
    obj = models.Teaching.objects.get(id=val)
    obj.delete()
    return HttpResponseRedirect('teaching_page')


def deletepublication(request):
    val = request.POST['deleteid']
    obj = models.Publications.objects.get(id=val)
    obj.delete()
    return HttpResponseRedirect('publications_page')


def deleteothers(request):
    val = request.POST['deleteid']
    obj = models.Others.objects.get(id=val)
    obj.delete()
    return HttpResponseRedirect('others_page')


def deleteprojects(request):
    val = request.POST['deleteid']
    obj = models.Projects.objects.get(id=val)
    obj.delete()
    return HttpResponseRedirect('projects_page')


def deletestudents(request):
    val = request.POST['deleteid']
    obj = models.Students.objects.get(id=val)
    obj.delete()
    return HttpResponseRedirect('students_page')


def deleteinvitedtalks(request):
    val = request.POST['deleteid']
    obj = models.Invitedtalks.objects.get(id=val)
    obj.delete()
    return HttpResponseRedirect('others_page')


def deleteresponsibilities(request):
    val = request.POST['deleteid']
    obj = models.Invitedtalks.objects.get(id=val)
    obj.delete()
    return HttpResponseRedirect('others_page')


def deleterecognition(request):
    val = request.POST['deleteid']
    obj = models.Recognitions.objects.get(id=val)
    obj.delete()
    return HttpResponseRedirect('recognitions_page')


def mail_crawl(request):
    file = open("IITG.html", "r")
    soup = bs4.BeautifulSoup(file, 'lxml')
    x = soup.find('pre').text
    y1 = re.search(r'Promote*', x, re.IGNORECASE)
    if y1 != None:
        y2 = re.search(r'head', x, re.IGNORECASE)
        y3 = re.search(r'associate prof*', x, re.IGNORECASE)
        y4 = re.search(r'assistant prof*', x, re.IGNORECASE)
        y5 = re.search(r'prof*', x, re.IGNORECASE)
        user = request.user
        if y2 != None:
            models.Faculty.objects.filter(user=user).update(designation="Head")
            # fac = models.Faculty.objects.get(user=user)
        elif y3 != None:
            models.Faculty.objects.filter(user=user).update(designation="Associate Professor")
        elif y4 != None:
            models.Faculty.objects.filter(user=user).update(designation="Assistant Professor")
        elif y5 != None:
            models.Faculty.objects.filter(user=user).update(designation="Professor")

    # file = open("recognitions.html", "r")
    # soup = bs4.BeautifulSoup(file, 'lxml')
    # x = soup.find('pre').text
    # y1 = re.search(r'recogni[sz]e*', x, re.IGNORECASE)
    # user = request.user
    # if y1 != None:
    #     y2 = x.split('"')[1].split('"')[0]
    #     y = x.split(y2)[1]
    #     y = y[1:]
    #     y3 = y.split('"')[1].split('"')[0]
    #     y = y.split(y3)[1]
    #     y = y[1:]
    #     y4 = y.split('"')[1].split('"')[0]
    #     # y3 = re.search(r'associate prof*', x, re.IGNORECASE)
    #     # y4 = re.search(r'assistant prof*', x, re.IGNORECASE)
    #     obj = models.Recognitions(recognition=y2, presenter=y3, year=y4)
    #     obj.user = user
    #     obj.save()
    return HttpResponseRedirect('basic_info')

# def signup(request):
#     # register = models.Faculty.objects.all()
#     template = loader.get_template('home/signup.html')
#     # context = {
#     #     'register':register,
#     # }
#     return HttpResponse(template.render({}, request))


# def submit(request):
#     if request.method == 'POST':
#         user_name = request.POST['user']
#         # password = request.POST['pass']
#         # success = user_name.check_password(request.POST['pass'])
#         # obj = models.Faculty(username=user_name, password=password)
#         # obj.save()
#         # if success:
#             return HttpResponseRedirect("/")
#         # else:
#         #     return HttpResponse("Your Password is incorrect")
#     else:
#         return HttpResponse("Error")
#     return HttpResponseRedirect("/")

# class UserFormView(View):
#     form_class = Userform
#     template_name = 'home/login.html'
#
#     # display blank form
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})
#
#     # process form data
#     def post(self, request):
#         form = self.form_class(request.POST)
#
#         if form.is_valid():
#
#             user = form.save(commit=False)
#
#             # cleaned data
#             username = form.changed_data['username']
#             password = form.changed_data['password']
#             user.set_password(password)
#             user.save()
#
#             # return User objects if crendentials are correct
#             user = authenticate(username=username, password=password)
#
#             if user is not None:
#
#                 if user.is_active:
#
#                     login(request, user)
#                     return redirect('home:home')
#
#         return render(request, self.template_name, {'form': form})



