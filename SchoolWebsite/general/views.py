from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from .models import Announcement, MemberInfo, MemberGrade, Course, Semester, Grade, Video, CourseProfessor
from .forms import StudentInfoForm, GradeForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
import json


# Create your views here.
def signup(request):
    if request.method == 'POST':
        signup_data = request.POST.dict()

        username = signup_data.get("username")
        password = signup_data.get("password")
        name = signup_data.get("name")
        group = signup_data.get("group")

        try:
            user = User.objects.create_user(username, email=None, password=password)
        except:
            return HttpResponseRedirect('/accounts/login')
        #user = authenticate(username=username, password=password)

        group = Group.objects.get(name=group)
        user.groups.add(group)
        user.save()
        newmemberinfo = MemberInfo(user=user)
        newmemberinfo.registrationstatus = 'R'
        newmemberinfo.name = name
        newmemberinfo.save()
        #login(request, user)
        return HttpResponseRedirect('../accounts/login/')
    return redirect('/accounts/login/')

def loginDefined(request):
    if request.method == 'POST':
        signup_data = request.POST.dict()

        username = signup_data.get("username")
        password = signup_data.get("password")
        user = authenticate(username=username, password=password)
        login(request,user)
        return redirect('/general/')
    return redirect('/accounts/login/')

"""
def signupprofessor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            group = Group.objects.get(name='Professor')
            user.groups.add(group)
            newmemberinfo = MemberInfo(user=user)
            newmemberinfo.registrationstatus = 'R'
            newmemberinfo.save()
            #login(request, user)
            return HttpResponseRedirect('../accounts/login/')
    else:
        form = UserCreationForm()
    return render(request, 'signupprofessor.html', {'form': form})
"""
def index(request):
    ann = Announcement.objects.all()

    context = {
        'ann': ann,
    }

    return render(request, 'index.html', context=context)

def displayinfo(request):
    try: 
        member = MemberInfo.objects.get(user = request.user)
    except MemberInfo.DoesNotExist:
        member = None
    context = {
        'pk': request.user.pk,
        'member': member
    }
    return render(request, 'displayinfo.html', context=context)

def editinfo(request):
    member = MemberInfo.objects.get(user = request.user)
    context = {
        'pk': request.user.pk,
        'name': member.name,
        'registrationstatus': member.registrationstatus,
        'contactinfo': member.contactinfo,
        'email': member.email,
        'address': member.address,
        'phone': member.phone,
        'form': StudentInfoForm(initial={
            'name': member.name,
            'registrationstatus': member.registrationstatus,
            'contactinfo': member.contactinfo,
            'email': member.email,
            'address': member.address,
            'phone': member.phone})
    }
    return render(request, 'editinfo.html', context=context)

def studentinfoedit(request):
    member = MemberInfo.objects.filter(user__pk = request.user.pk).first()
    form = StudentInfoForm(request.POST, instance=member)
    if form.is_valid():
        member = form.save()
        member.save()
        context={'form': form,
            'pk': request.user.pk,
            'member': member,
        }
        return redirect('/general/displayinfo')
    return render(request, 'displayinfo.html', context)

def editgrade(request, pk):
    grade = MemberGrade.objects.filter(pk = pk)
    form = GradeEditForm(request.POST)
    if form.is_valid():
        grade = form.save()
        grade.save()
        context={'form': form,
            'membergrade': grade,
        }
        return redirect('/general/displaygrades')
    return render(request, 'displaygrades.html', {'form': form})

def displaygrades(request):
    try: 
        member = MemberGrade.objects.filter(user = request.user)
    except MemberGrade.DoesNotExist:
        member = None
    context = {
        'membergrade_list': member
    }
    return render(request, 'displaygrades.html', context=context)

def managegrades(request):
    try:
        cp = CourseProfessor.objects.filter(professor = request.user).values_list('course_id', flat=True)
        courses = Course.objects.filter(pk__in=cp)
        membergrades = MemberGrade.objects.filter(course__in=courses)
        memberinfo = MemberInfo.objects.all()
    except (Course.DoesNotExist or MemberGrade.DoesNotExist):
        courses = None
        membergrades = None
    context = {
        'courses': courses,
        'membergrades': membergrades,
        'memberinfo': memberinfo
    }
    return render(request, 'managegrades.html', context=context)

def editgrades(request, pk):
    editgrade = MemberGrade.objects.get(pk=pk)
    grades = Grade.objects.all()
    memberinfo = MemberInfo.objects.all()
    try: 
        cp = CourseProfessor.objects.filter(professor = request.user).values_list('course_id', flat=True)
        courses = Course.objects.filter(pk__in=cp)
        membergrades = MemberGrade.objects.filter(course__in=courses)
    except (Course.DoesNotExist):
        courses = None
    except (MemberGrade.DoesNotExist):
        membergrades = None
    context = {
        'user': request.user,
        'courses': courses,
        'membergrades': membergrades,
        'memberinfo': memberinfo,
        'editgrade': editgrade,
        'grades': grades
    }
    return render(request, 'editgrades.html', context=context)

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)

def uploadvideo(request):
    cp = CourseProfessor.objects.filter(professor = request.user).values_list('course_id', flat=True)
    courses = Course.objects.filter(pk__in=cp)
    videos = Video.objects.filter(professor=request.user)

    context = {
        'courses': courses
    }

    return render(request, 'videos.html', context)

def showvideo(request, courseid, lectureno, videoname):

    # upload video to youtube
    #execfile('upload_video.py 
    #           --file= videopath
    #           --title=videoname 
    #           --keywords="lecture " + lectureno + " " + videoname
    #           --category="22"
    #           --privacyStatus="private"')

    course = Course.objects.filter(pk = courseid).first()

    # video 정보 DB에 저장
    v = Video(name=videoname, professor=request.user, course=course, lectureno=lectureno)
    v.save()

    context = {
        'video': v
    }
    return render(request, 'showvideo.html', context)
    
def regcourses(request):
    try: 
        member = MemberGrade.objects.filter(user = request.user)
        m_courses = MemberGrade.objects.filter(user = request.user).values_list('course', flat=True)
        courses = Course.objects.all().exclude(pk__in=m_courses)
    except MemberGrade.DoesNotExist:
        member = None
        courses = Course.objects.all()

    context = {
        'upk': request.user.pk,
        'membergrade_list': member,
        'courses': courses,
        'semesters': Semester.objects.all()
    }
    return render(request, 'regcourses.html', context=context)

def registercourses(request):
    courselist = request.POST.getlist('course')

    for cours in courselist:
        g = MemberGrade.objects.create(user = request.user, course=Course.objects.get(pk=cours)
        ,semester=Semester.objects.get(pk=request.POST.get("sem","")))
        g.save()

    return redirect('/general/regcourses/' + str(request.user.pk))

## return list of courses that is not registered by student & registration is open
## 학생이 등록 하지 않았고 등록 가능한 수업 리스트 
@csrf_exempt
def courses(request):

    userob = User.objects.get(pk=request.user.pk)
    
    m_courses = MemberGrade.objects.filter(user = userob).values_list('course', flat=True)
    print(m_courses)
    # Get the objects from the database
    rawData = Course.objects.filter(semester__year=request.POST.get('year'), semester__type=request.POST.get('type')).exclude(pk__in=m_courses)
    print(rawData)
    # Create array
    json_res = []

    # Iterate over results and add to array
    for record in rawData: 
        json_obj = dict(name = record.name, id=record.id, professor=record.professor.username)
        json_res.append(json_obj)

    # Return the results   		
    return HttpResponse(json.dumps(json_res), content_type='application/json')

@csrf_exempt
def submitgrade(request, pk):
    grade_data = request.POST.dict()
    try: 
        cp = CourseProfessor.objects.filter(professor = request.user).values_list('course_id', flat=True)
        courses = Course.objects.filter(pk__in=cp)
        membergrades = MemberGrade.objects.filter(course__in=courses)
        editgrade = MemberGrade.objects.get(pk=pk)
    except (Course.DoesNotExist):
        courses = None
    except (MemberGrade.DoesNotExist):
        membergrades = None
    grade = grade_data.get("grade")
    editgrade.grade = Grade.objects.get(value=grade)
    editgrade.save()
    return redirect('/general/managegrades')

def redirect_view(request):
    response = redirect('index')
    return response

def edit_announcements(request):

    memberinfo = MemberInfo.objects.filter(user=request.user).first()

    context = {
        'memberinfo': memberinfo
    }
    return render(request, 'announcement.html', context=context)

def post_announcements(request):
    if request.method == 'POST':
        ann_data = request.POST.dict()
        title = ann_data.get("title")
        info = ann_data.get("info")

        ann = Announcement(writer=request.user, title=title, information=info)
        ann.save()

    context = {
        'announcement': ann
    }

    return render(request, 'done_announcement.html', context=context)

def videolecture(request):
    return render(request, 'videolecture.html')