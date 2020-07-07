from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),
    path('displayinfo', views.displayinfo, name='displayinfo'),
    path('editinfo', views.editinfo, name='editinfo'),
    path('edit', views.studentinfoedit, name='studentinfoedit'),
    path('displaygrades', views.displaygrades, name='displaygrades'),
    path('managegrades', views.managegrades, name='managegrades'),
    path('editgrades/<int:pk>', views.editgrades, name='editgrades'),
    path('editgrade/<int:pk>', views.editgrade, name='editgrade'),
    path('regcourses', views.regcourses, name='regcourses'),
    path('registercourses', views.registercourses, name='registercourses'),
    path('courses', views.courses, name='courses'),
    path('submitgrade/<int:pk>', views.submitgrade, name='submitgrade'),
    path('video', login_required(views.uploadvideo), name='uploadvideo'),
    path('showvideo/<str:courseid>/<str:lectureno>/<str:videoname>', views.showvideo, name='showvideo'),
    path('edit_announcements', views.edit_announcements, name='edit_announcements'),
    path('post_announcements', views.post_announcements, name='post_announcements'),
    path('videolecture', views.videolecture, name='videolecture'),
]

