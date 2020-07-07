from django.db import models
from django.contrib.auth.models import User, Group

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    information = models.CharField(max_length=500)
    writer = models.ForeignKey(User, on_delete = models.DO_NOTHING)

    def __str__(self):
        return self.title

class Grade(models.Model):
    LETTERGRADES = (
        ('A', 'Excellent'),
        ('B', 'Good'),
        ('C', 'Average'),
        ('D', 'Poor'),
        ('F', 'Fail')
    )
    value = models.CharField(max_length=1, choices=LETTERGRADES)

    def __str__(self):
        return self.value

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class DepartmentProfessor(models.Model):
    department = models.ForeignKey(Department, on_delete = models.DO_NOTHING)
    professor = models.ForeignKey(User, limit_choices_to={'groups__name': "Professor"}, on_delete = models.DO_NOTHING)

    def __str__(self):
        return self.department + ": " + self.professor.username

class Semester(models.Model):
    SEASON = (
        ('FA', 'Fall'),
        ('SP', 'Spring')
    )
    year = models.CharField(max_length = 4)
    type = models.CharField(max_length=4, choices=SEASON)
    regopen = models.BooleanField()

    def __str__(self):
        return self.year + " " + str(self.type)

class Course(models.Model):
    name = models.CharField(max_length=100)
    credits = models.IntegerField()

    def __str__(self):
        return self.name

class CourseProfessor(models.Model):
    professor = models.ForeignKey(User, limit_choices_to={'groups__name': "Professor"}, on_delete = models.DO_NOTHING)
    course = models.ForeignKey(Course, on_delete = models.DO_NOTHING)
    semester = models.ForeignKey(Semester, on_delete = models.DO_NOTHING)

    def __str__(self):
        return MemberInfo.objects.filter(user=self.professor).first().name + " " + self.course.name + " " + str(self.semester)

class MemberGrade(models.Model):
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    semester = models.ForeignKey(Semester, on_delete = models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.DO_NOTHING)
    grade = models.ForeignKey(Grade, on_delete = models.CASCADE, null=True, blank=True)

class MemberInfo(models.Model):

    REGISTERED = 'RE'
    UNREGISTERED = 'UR'

    REGSTATUS = (
        (REGISTERED, 'Registered'),
        (UNREGISTERED, 'Unregistered')
    )

    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    name = models.CharField(max_length=10)
    registrationstatus = models.CharField(
        max_length=12,
        choices=REGSTATUS,
        default=UNREGISTERED,
        )
    contactinfo = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    name= models.CharField(max_length=500)
    professor = models.ForeignKey(User, limit_choices_to={'groups__name': "Professor"}, on_delete = models.DO_NOTHING)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    lectureno = models.IntegerField()

    def __str__(self):
        return self.name